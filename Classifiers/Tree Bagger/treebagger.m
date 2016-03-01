function [] = treebagger()

clear
clc
temp=ourdata();
accu=zeros(size([50:10:950]));
count=1;
for qw=[50:10:950]

temp=temp(randperm(size(temp,1)),:);
train=temp(1:qw,:);
datatrain=train(:,1:size(train,2)-1);
classtrain=train(:,size(train,2));
test=temp(qw+1:size(temp,1),:);
datatest=test(:,1:size(test,2)-1);
classtest=test(:,size(test,2));
b = TreeBagger(20,datatrain,classtrain,'Method','Classification');
x = b.predict(datatest);
y = cell2mat(x);
y = str2num(y);
accu(count)=100*size(find(y==classtest),1)/size(y,1);
100*size(find(y==classtest),1)/size(y,1)
count=count+1;
end
save ('accubagger.mat','accu');
plot([50:10:950],accu);





end
function [data]=ourdata()
fileID = fopen('data.txt');
% class=
data = textscan(fileID,'%f %f %f %f %f %f %f %f %f %f %f');
fileID = fopen('lables.txt');
class=textscan(fileID,'%f');
% dataset = rdivide(data{1},max(data{1}));
dataset=[];
for i = 1:11
    if i~=1
        dataset = horzcat(dataset,rdivide(data{i},max(data{i})));
    else
        dataset = horzcat(dataset,rdivide(data{i},1));
    end
end
data = horzcat(dataset, class{1});
end
