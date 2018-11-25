function [steve2,diagKs,realfr]=mtxread_mk2
stiff=load('Frequency_STIF1.mtx');
mass=load('Frequency_MASS1.mtx');
num_nodes=3636;
Ms1=sparse(mass(:,1),mass(:,2),mass(:,3));
Ks1=sparse(stiff(:,1),stiff(:,2),stiff(:,3));
diagKs=find(diag(Ks1)==1e36);
Ms=Ms1;Ks=Ks1;
Ms(diagKs,:)=[];
Ks(diagKs,:)=[];
Ks(:,diagKs)=[];
Ms(:,diagKs)=[];
[e11,e12]=eigs((Ms\Ks),3600,'smallestabs');
N=e11.'*Ms*e11;
diagN=diag(N);
steve=zeros(num_nodes-length(diagKs));
for i=1:num_nodes-length(diagKs)
    steve(:,i)=e11(:,i)./sqrt(diagN(i));
end
[fr,idx]=sort(sqrt(diag(e12)));
realfr=real(fr);
steve2=steve(:,idx);
end