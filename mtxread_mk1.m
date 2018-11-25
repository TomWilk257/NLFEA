function [steve2,realfr,diagKs,Ms1]=mtxread_mk1
stiff=load('Frequency_STIF1.mtx');
mass=load('Frequency_MASS1.mtx');
num_nodes=3636;
% Ms=sparse(mass(:,1),mass(:,2),mass(:,3));
% Ks=sparse(stiff(:,1),stiff(:,2),stiff(:,3));
Ks1=zeros(num_nodes);
for i=1:size(stiff,1)
    Ks1(stiff(i,1),stiff(i,2))=stiff(i,3);
end
Ms1=zeros(num_nodes);
for i=1:size(mass,1)
    Ms1(mass(i,1),mass(i,2))=mass(i,3);
end
diagKs=find(diag(Ks1)==1e36);
Ms=Ms1;Ks=Ks1;
Ms(diagKs,:)=[];
Ks(diagKs,:)=[];
Ks(:,diagKs)=[];
Ms(:,diagKs)=[];
%Eigen Values and Vectors
[e11,e12]=eig(Ms\Ks);
N=e11.'*Ms*e11;
diagN=diag(N);
steve=zeros(num_nodes-length(diagKs));
for i=1:num_nodes-length(diagKs)
    steve(:,i)=e11(:,i)./sqrt(diagN(i));
end
%Update Eigen Vectors
Iden=round(steve'*Ms*steve,1);
%Frequencies
[fr,idx]=sort(sqrt(diag(e12)));
realfr=real(fr);
steve2=steve(:,idx);
%modal force to the first mode
% f=zeros(length(realfr),1);
% f(1)=modeforce;
% realf=steve*f;
% fbigfinal=zeros(length(Ms1),1);
% %real forces
% %steve2=zeros(length(Ms1));
% len1=1:1:length(Ms1);
% w1=~ismember(len1,diagKs);
% fbigfinal(w1)=realf;
% %steve2(w1,w1)=steve;
% %freal=inv(steve2')*fbig;
% fbigfinalfinal=reshape(fbigfinal,[3 length(fbigfinal)/3]).';
% q1=(fbigfinalfinal==0);
% fbigfinalfinal(q1)=1e-36;
% csvwrite('myFile2.csv',fbigfinalfinal);
end