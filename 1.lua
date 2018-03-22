
local GRU,parent = torch.class('seqmatchseq.GRU','nn.Module')

function GRU:__init(config)
    parent.__init(self)

    self.in_dim = config.in_dim
    self.mem_dim = config.mem_dim or 150

    if config.output_gate ~= nil then self.output_gate = config.output_gate else self.output_gate = true end

    self.master_cell = self:new_cell()
    self.depth = 0
    self.hOutput = torch.Tensor()
    self.cells = {}

    self.initial_values = {torch.zeros(self.mem_dim)}
    self.gradInput = { torch.zeros(self.in_dim),torch.zeros(self.mem_dim) }
end

function GRU:new_cell()   
    local input = nn.Identity()() 
    local h_p = nn.Identity()()

    local new_gate = function()
        return nn.CAddTable(){
            nn.Linear(self.in_dim, self.mem_dim)(input),
            nn.Linear(self.mem_dim, self.mem_dim)(h_p)
        }
    end

    local update_gate = nn.Sigmoid()(new_gate())
    local reset_gate = nn.Sigmoid()(new_gate())
    -- compute candidate hidden state
    local gated_hidden = nn.CMulTable()({reset_gate, h_p})
    local p2 = nn.Linear(self.mem_dim, self.mem_dim)(gated_hidden)
    local p1 = nn.Linear(self.in_dim, self.mem_dim)(input)
    local hidden_candidate = nn.Tanh()(nn.CAddTable()({p1,p2}))
    -- compute new interpolated hidden state, based on the update gate
    local zh = nn.CMulTable()({update_gate, hidden_candidate})
    local zhm1 = nn.CMulTable()({nn.AddConstant(1,false)(nn.MulConstant(-1,false)(update_gate)), h_p})
    local output = nn.CAddTable()({zh, zhm1})
    

    local cell = nn.gModule({input,h_p}, {output})

    if self.master_cell then
        share_params(cell, self.master_cell)
    end
    return cell
end



function GRU:forward(inputs, reverse) 
    
    
    local size = inputs:size(1)
    self.hOutput:resize(size, self.mem_dim)
    for t = 1, size do
	local outputs = {}
        local prev_output ={}
        local idx = reverse and size-t+1 or t
        local input = inputs[idx] 
	
        self.depth = self.depth + 1
        local cell = self.cells[self.depth] 
        if cell == nil then
            cell = self:new_cell()
	    --print(idx)
	    --print(self.depth)
            self.cells[self.depth] = cell
        end
        table.insert(prev_output,self.depth > 1 and self.cells[self.depth - 1].output or      self.initial_values)


	if self.depth == 1 then 
	    --print('A',self.depth,prev_output,type(prev_output))
            table.insert(outputs,cell:forward({input,prev_output[1][1]}))
	end
	if self.depth > 1 then 
	    --print('B',self.depth,prev_output,type(prev_output))
            table.insert(outputs,cell:forward({input,prev_output[1]}))
	end
	--print('C',self.depth,outputs,type(outputs))
        local h = unpack(outputs)
        self.output = h
        self.hOutput[idx] = h
	
    end

    return self.output
end

function GRU:backward(inputs, grad_outputs, reverse)  -----return input_grads
    local size = inputs:size(1)
    assert(self.depth ~= 0)  -----  ~=是！=

    local input_grads = torch.Tensor(inputs:size())
    for t = size, 1, -1 do
        local idx = reverse and size-t+1 or t
        local input = inputs[idx]
        local grad_output = grad_outputs[idx]

        local cell = self.cells[self.depth]
        local grads = {self.gradInput[2]}
        grads[1]:add(grad_output)

        local prev_output = self.depth > 1 and self.cells[self.depth - 1].output or self.initial_values

        self.gradInput = cell:backward({input, prev_output[1]}, grads[1])

        input_grads[idx] = self.gradInput[1]

        self.depth = self.depth - 1
    end

    --self:forget()

    return input_grads
end

function GRU:share(gru,...)
    assert( self.in_dim == gru.in_dim )
    assert( self.mem_dim == gru.mem_dim )
    share_params(self.master_cell, gru.master_cell,...)
end

function GRU:zeroGradParameters()
    self.master_cell:zeroGradParameters()
end

function GRU:parameters()
    return self.master_cell:parameters()
end

