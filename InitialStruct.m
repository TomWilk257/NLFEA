tic
%Run freq. analysis of case, built into Freq_Analysis.py
dos('abaqus cae noGUI=Freq_Analysis.py');
[Phi,Lam,Midx,diagKs]=Get_Modal_v2;
%Run matlab file to convert mass and stiff matrices to get modal forces as
%.csv file to plug back into next abaqus file
p=0;
af=linspace(-1,1,10);
for k= 5e-2:2e-1:2e+0
    for i = 1:length(af)
        p=p+1;
        forcecalc(Phi,Lam,Midx,diagKs,af(i)*k)
        %Get modal displacements 
        dos('abaqus cae noGUI=Freq_Analysis_Copy.py');
        %Extract results from previous step
        dos('abaqus cae noGUI=readdispoutput.py');
        movefile('results1.csv',['force',num2str(p),'.csv'],'f');
        p
    end
end
toc