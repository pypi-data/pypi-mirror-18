%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best biclique from preprocessed information on the non-covered graph
% Input graph should be a bipartite graph.
%
% Constants:
%       - cc: treated connected component. (cc/1 gives existing cc)
%       -  k: current step of treatment (first step is 1)
% Input:
%       - inter(X,Y): there exist an edge linking X and Y in cc.
%       - edge(X,Y): there exist an oriented edge linking X and Y in cc.
%       - membercc(Y): Y is a member of cc.
% Output:
%       - newconcept(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - star(cc,k,T): set T of concept is a star.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

