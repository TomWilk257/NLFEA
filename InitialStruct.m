tic
%Run freq. analysis of case, built into Freq_Analysis.py
dos('abaqus cae noGUI=Freq_Analysis.py');

%Run matlab file to convert mass and stiff matrices to get modal forces as
%.csv file to plug back into next abaqus file
for i = 1:10
mtxread_mk1(i);

%Get modal displacements 
dos('abaqus cae noGUI=Freq_Analysis_Copy.py');

%Extract results from previous step
dos('abaqus cae noGUI=readdispoutput.py');
movefile('results1.csv',['Modeshape',num2str(i),'.csv']);
i
end
toc