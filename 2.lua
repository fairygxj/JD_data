--[[
Copyright 2015 Singapore Management University (SMU). All Rights Reserved.

Permission to use, copy, modify and distribute this software and its documentation for purposes of research, teaching and general academic pursuits, without fee and without a signed licensing agreement, is hereby granted, provided that the above copyright statement, this paragraph and the following paragraph on disclaimer appear in all copies, modifications, and distributions.  Contact Singapore Management University, Intellectual Property Management Office at iie@smu.edu.sg, for commercial licensing opportunities.

This software is provided by the copyright holder and creator “as is” and any express or implied warranties, including, but not Limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed.  In no event shall SMU or the creator be liable for any direct, indirect, incidental, special, exemplary or consequential damages, however caused arising in any way out of the use of this software.
]]


local GRUwwatten, parent = torch.class('seqmatchseq.GRUwwatten', 'nn.Module')

function GRUwwatten:__init(config)
    parent.__init(self)
    self.mem_dim       = config.mem_dim       or 150
    self.att_dim       = config.att_dim       or self.mem_dim
    self.in_dim       = config.in_dim       or self.mem_dim

    self.master_ww = self:new_ww()
    self.depth = 0
    self.wws = {}

    self.initial_values = {torch.zeros(self.in_dim)}
    self.gradInput = {
        torch.zeros(self.mem_dim),
        torch.zeros(self.mem_dim),
        torch.zeros(self.mem_dim)
    }

    self.hOutput = torch.Tensor()
end

function GRUwwatten:new_ww()

    local linput, rinput, m_p  = nn.Identity()(), nn.Identity()(), nn.Identity()()
    --padding
    local lPad = nn.Padding(1,1)(linput)
    local M_l = nn.Linear(self.in_dim, self.att_dim)(lPad)

    local M_r = nn.Linear(self.in_dim, self.att_dim)(rinput)
    local M_a = nn.Linear(self.mem_dim, self.att_dim)(m_p)

    local M_ra =  nn.CAddTable(){M_r, M_a}
    local M = nn.Tanh()(nn.CAddRepTable(){M_l, M_ra})

    local wM = nn.Linear(self.att_dim, 1)(M)
    local alpha = nn.SoftMax()( nn.View(-1)(wM) )

    local Yl =  nn.MV(true){lPad, alpha}

    local new_gate = function()
        return nn.CAddTable(){
            nn.Linear(self.mem_dim, self.mem_dim)(m_p),
            nn.Linear(self.in_dim, self.mem_dim)(rinput),
            nn.Linear(self.in_dim, self.mem_dim)(Yl)
        }
    end
    

    local update_gate = nn.Sigmoid()(new_gate())
    local reset_gate = nn.Sigmoid()(new_gate())
    local gated_hidden = nn.CMulTable()({reset_gate, m_p})
    local p2 = nn.Linear(self.mem_dim, self.mem_dim)(gated_hidden)
    local p1 = nn.Linear(self.in_dim, self.mem_dim)(rinput)
    local hidden_candidate = nn.Tanh()(nn.CAddTable()({p1,p2}))
    -- compute new interpolated hidden state, based on the update gate
    local zh = nn.CMulTable()({update_gate, hidden_candidate})
    local zhm1 = nn.CMulTable()({nn.AddConstant(1,false)(nn.MulConstant(-1,false)(update_gate)), m_p})
    local next_h = nn.CAddTable()({zh, zhm1})


    local ww = nn.gModule({linput, rinput, m_p}, {next_h})

    if self.master_ww then
        share_params(ww, self.master_ww)
    end
    return ww
end

function GRUwwatten:forward(inputs, reverse)
    local lHinputs, rHinputs = unpack(inputs)
    local size = rHinputs:size(1)
    self.hOutput:resize(size, self.mem_dim)
    local prev_output ={}
    local prev_output = {}
    for t = 1, size do
	
        local idx = reverse and size-t+1 or t
        self.depth = self.depth + 1
        local ww = self.wws[self.depth]
        if ww == nil then
            ww = self:new_ww()
            self.wws[self.depth] = ww
        end
	--table.insert(prev_output,(self.depth > 1) and self.wws[self.depth - 1].output
                                            --or self.initial_values)
        local prev_output = (self.depth > 1) and self.wws[self.depth - 1].output
                                            or self.initial_values
	local output = {}
	if self.depth == 1 then
	    --print('A',self.depth,prev_output,type(prev_output))
	    table.insert(output,ww:forward({lHinputs, rHinputs[idx], unpack(prev_output)}))
	end
	if self.depth > 1 then
	    --print('B',self.depth,self.wws[self.depth - 1].output,type(self.wws[self.depth - 1].output))
	    table.insert(output,ww:forward({lHinputs, rHinputs[idx], prev_output}))
	end
	
	
        
	--if self.depth == 1 then
             --table.insert(output,ww:forward({lHinputs, rHinputs[idx], unpack(prev_output[1])}))
	--end
	--if self.depth > 1 then
	     --print('B',self.depth,prev_output,type(prev_output[self.depth]))
	     --table.insert(output,ww:forward({lHinputs, rHinputs[idx], prev_output[self.depth]}))
	--end
	--print('-----------------------',type(output))
        self.hOutput[idx] = output[1]
        self.output = output
    end
    return self.output
end

function GRUwwatten:backward(inputs, grad_outputs, reverse)
    local lHinputs, rHinputs = unpack(inputs)
    local size = rHinputs:size(1)
    local grad_lHinputs = torch.zeros(lHinputs:size())
    local grad_rHinputs = torch.zeros(rHinputs:size())
    assert( self.depth ~= 0 )

    for t = size, 1, -1 do
        local idx = reverse and size-t+1 or t
        local ww = self.wws[self.depth]
        local grad = {self.gradInput[3]}
        grad[1]:add(grad_outputs[idx])

        local prev_output = {}
	table.insert(prev_output,(self.depth > 1) and self.wws[self.depth - 1].output
                                             or self.initial_values)
        self.gradInput = ww:backward({lHinputs, rHinputs[idx], unpack(prev_output)}, grad[1])

        grad_lHinputs:add(self.gradInput[1])
        grad_rHinputs[idx] = self.gradInput[2]

        self.depth = self.depth - 1
    end
    --self:forget()

    return {grad_lHinputs, grad_rHinputs}
end



function GRUwwatten:share(GRUwwatten)
    assert( self.att_dim == GRUwwatten.att_dim )
    assert( self.mem_dim == GRUwwatten.mem_dim )
    share_params(self.master_ww, GRUwwatten.master_ww)
end

function GRUwwatten:zeroGradParameters()
    self.master_ww:zeroGradParameters()
end

function GRUwwatten:parameters()
    return self.master_ww:parameters()
end


