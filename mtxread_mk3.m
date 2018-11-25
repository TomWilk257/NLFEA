function mtxread_mk3(realfr,Ms1,diagKs,steve2,modeforce)
f=zeros(length(realfr),1);
f(1)=modeforce;
realf=real(steve2'\f);
fbigfinal=zeros(length(Ms1),1);
%real forces
%steve2=zeros(length(Ms1));
len1=1:1:length(Ms1);
w1=~ismember(len1,diagKs);
fbigfinal(w1)=realf;
%steve2(w1,w1)=steve;
%freal=inv(steve2')*fbig;
fbigfinalfinal=reshape(fbigfinal,[3 length(fbigfinal)/3]).';
q1=(fbigfinalfinal==0);
fbigfinalfinal(q1)=1e-36;
csvwrite('myFile2.csv',fbigfinalfinal);
end