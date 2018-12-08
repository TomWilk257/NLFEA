function forcecalc(Phi,Lam,N,diagKs,appforce)
f=zeros(length(Lam),1);
f(1)=appforce;
realf=real(Phi.'\f);
fbigfinal=zeros(length(N),1);
len1=1:1:N;
w1=~ismember(len1,diagKs);
fbigfinal(w1)=realf;
fbigfinalfinal=reshape(fbigfinal,[3 length(fbigfinal)/3]).';
q1=(fbigfinalfinal==0);
fbigfinalfinal(q1)=1e-36;
csvwrite('myFile2.csv',fbigfinalfinal);
end