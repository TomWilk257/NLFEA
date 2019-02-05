tic
%Run freq. analysis of case, built into Freq_Analysis.py
dos('abaqus cae noGUI=Freq_Analysis.py');
[Phi,Lam,N,diagKs]=Get_Modal_v2;
%Run matlab file to convert mass and stiff matrices to get modal forces as
%.csv file to plug back into next abaqus file
p=0;
af=linspace(-1,1,10);
excite=[1];
sf=1e-1:1e-1:1e+0;
for k= 1
    for i = 1
        p=p+1;
        forcecalc(Phi,Lam,N,diagKs,af(i)*sf(k),excite);
        %Get modal displacements 
        dos('abaqus cae noGUI=Freq_Analysis_Copy.py');
        %Extract results from previous step
        %delete('myFile2.csv');
        dos('abaqus cae noGUI=readdispoutput.py');
        %pause(10);
        movefile('results1.csv',['force','_',num2str(k),'_',num2str(i),'.csv'],'f');
        p
    end
end

toc