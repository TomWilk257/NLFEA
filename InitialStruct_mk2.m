clear;
clc;
close;

tic
%Run freq. analysis of case, built into Freq_Analysis.py
dos('abaqus cae noGUI=Freq_Analysis.py');
[Phi,Lam,N,diagKs]=Get_Modal_v2;
%Run matlab file to convert mass and stiff matrices to get modal forces as
%.csv file to plug back into next abaqus file
p=0;
af=linspace(-1,1,10);
sf=1e-1:1e-1:1e+0;
for k= 1:length(sf)
    for i = 1:length(af)
        p=p+1;
        forcecalc(Phi,Lam,N,diagKs,af(i)*sf(k))
        %Get modal displacements 
        dos('abaqus cae noGUI=Mode_Shape.py');
        %Extract results from previous step
        %delete('myFile2.csv');
        dos('abaqus cae noGUI=readdispoutput.py');
        movefile('C:/temp/results1.csv',['force','_',num2str(k),'_',num2str(i),'.csv'],'f');
        p
    end
end
toc

readdispresults_mk1


