function [Phi,Lam,N,diagKs]=Get_Modal_v2
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

tic
load('Frequency_MASS1.mtx')
load('Frequency_STIF1.mtx')
toc

%%%%%%%%%%%%%%%%%%%%

tic

N = max(Frequency_MASS1(:,1));
M = zeros(N);
K = zeros(N);

Midx = sub2ind([N,N],Frequency_MASS1(:,1),Frequency_MASS1(:,2));
Kidx = sub2ind([N,N],Frequency_STIF1(:,1),Frequency_STIF1(:,2));

M(Midx) = Frequency_MASS1(:,3);
K(Kidx) = Frequency_STIF1(:,3);

[idx,~] = find(K == 1e36);
diagKs=idx;
M(idx,:) = [];
M(:,idx) = [];
K(idx,:) = [];
K(:,idx) = [];

disp(max(K(:)))

[Phi,Lam] = eig(K,M);

Lam = diag(Lam);
[~,idx] = sort(abs(Lam));
Lam = diag(Lam(idx));
Phi = Phi(:,idx);

%Lam(1:10,1:10)
%Phi(1:10,1:10)

%max(max(abs( Phi.'*M*Phi - eye(size(M)) )))


%nonzeros(imag(Phi))

toc
