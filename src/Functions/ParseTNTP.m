function [G] = ParseTNTP(pathDataFolder, nameNetwork)

% extract path prefix of data files
pathDataPrefix = [pathDataFolder, nameNetwork, '\', nameNetwork, '_'];

% construct paths of data files
pathDataNode    = [pathDataPrefix,  'node', '.tntp'];
pathDataNetwork = [pathDataPrefix,   'net', '.tntp'];

% read tab-delimited files
dataNode    = tdfread(pathDataNode,    '\t');
dataNetwork = tdfread(pathDataNetwork, '\t');

% store link data
nodeInit = dataNetwork.init_node;
nodeTerm = dataNetwork.term_node;
linkCap  = dataNetwork.capacity;
linkLen  = dataNetwork.length;
linkFFT  = dataNetwork.free_flow_time;
linkB    = dataNetwork.b;
linkPow  = dataNetwork.power;

% store node data
X        = dataNode.X;
Y        = dataNode.Y;

% define auxiliary variable
ODs     = [nodeInit, nodeTerm];

% define names of table columns
nameVarsEdge = {'EndNodes', 'Capacity', 'Length', 'FreeFlowTime', 'B', 'Power'};
nameVarsNode = {'X', 'Y'};

% construct node table and edge table
NodeTable = table(X, Y, 'VariableNames', nameVarsNode);
EdgeTable = table(ODs, linkCap, linkLen, linkFFT, linkB, linkPow, 'VariableNames', nameVarsEdge);

% generate digraph object
G = digraph(EdgeTable, NodeTable); % caution: edges will be rearranged

end