clear all
clc
n=importdata('new');
d=importdata('data.txt');
l=importdata('truth.txt');
l1=regexp(l,' ','split');
l=[];
for i=[1:size(l1)]
    l=[l;l1{i,:}];
end
lab=l(:,2);
accuracyr=[];
lab=cell2mat(lab);
for i=linspace(50,950,91)
    newtrain=d(1:i,:);
    class_train=lab(1:i);
    newtest=d(i+1:end,:);
    class_test=lab(i+1:end);
    svmS=svmtrain(newtrain,class_train,'kernel_function','rbf');
    accuracyr(i) = ((size(find((svmclassify(svmS,newtest) == class_test) == 1), 1))*100)/(size(newtest,1));
end
