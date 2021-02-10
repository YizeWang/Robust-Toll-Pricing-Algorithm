function [ABig, bBig] = GetEqualityConstraints(G, ODs)

% extract dimensions
numNode = G.numnodes;
numEdge = G.numedges;
numDmnd = size(ODs, 1);

% use memory-saving sparse matrix
A = sparse(numNode, numEdge);
b = sparse(numNode, numDmnd);

% construct matrix A
for n = 1:numNode
    edgeIn  =  inedges(G, n); % row index in edge table
    edgeOut = outedges(G, n); % row index in edge table
    
    A(n, edgeIn)  =  1; % sum of inedge flows
    A(n, edgeOut) = -1; % sum of outedge flows
end

% construct matrix b
for k = 1:numDmnd
    s = ODs(k, 1);
    t = ODs(k, 2);
    d = ODs(k, 3);
    
    b(s, k) = -d;
    b(t, k) =  d;
end

% augmented matrix A (x stacked into vector)
A11                        =  -eye(numEdge); %        |     |         |
A12      = repmat(eye(numEdge), 1, numDmnd); %        | A11 |   A12   | 
A21      = sparse(numNode*numDmnd, numEdge); %        |-----+---------|
ACell             = repmat({A}, numDmnd, 1); % ABig = |     |         |     
A22                     = blkdiag(ACell{:}); %        | A21 |   A22   |       
ABig                 = [A11, A12; A21, A22]; %        |     |         |

% augmented vector b (x stacked into vector)
bBigDown = reshape(b, [numNode*numDmnd, 1]); % bBD  = [b1; ... ; bK]
bBig       = [sparse(numEdge, 1); bBigDown]; % bBig = [0; bBD];

end