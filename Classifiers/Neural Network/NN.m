function [] = NN()

clear
clc
%{
file= fopen('optdigits.tra');
s='%f';
for i=1:64
    s=strcat(s,',%f');
end
data = textscan(file,s);
a=data{1};
for i=2:65
    a=[a data{i}];
end
new=a(1,:);
for i=2:size(a,1)
    if mod(a(i,65),7)==0
        new=[new;a(i,:)];
    end
end
%}
accu=zeros(size([20:10:900]));
xy=1;
for qw=[20:10:900]
temp=ourdata();
temp=temp(randperm(size(temp,1)),:);
new=temp(1:qw,:);
hidden=50;
in=size(temp,2);
out=2;
%%initializers
w1=((rand(hidden,in)*2)-1)/(sqrt(in));
w2=((rand(out,hidden)*2)-1)/(sqrt(8));
X=[zeros(size(new,1),1)+1 new(:,1:in-1)];
class=new(:,in);
i=0;
eta=1;
counter=0;
last=0;
maxx=0;
minn=20000;
new_cnt=0;
pre=0;
new=0;
maxxxxxxxx=0;
while 1>0
    
    ind=mod(i,size(X,1))+1;
    new=floor(i/size(X,1));
    if(new-pre==1)
        pre=new;
        
        maxxxxxxxx=max(maxxxxxxxx,new_cnt);
        
        new_cnt=0;
    end
    t=[class(ind) ~(class(ind))];
    x=X(ind,:);
    netj=x*w1';
    y=zeros(size(netj,1),size(netj,2));
    y_=zeros(size(netj,1),size(netj,2));
    y=1./(1+exp(-netj));
    y_=y-(y.*y);
    netk=y*w2';
    z=zeros(size(netk,1),size(netk,2));
    z_=zeros(size(netk,1),size(netk,2));
    z=1./(1+exp(-netk));
    z_=z-(z.*z);
    %%BACK PROPOGATION
    delw2=eta*((t-z).*z_)'*y;
    delw1=eta*((((t-z).*z_)*w2).*y_)'*x;
    w2=w2+delw2;
    w1=w1+delw1;
    i=i+1;
    error=0;
    %CALC J(W)
    

       %{
        for cc=1:size(X,1)
            t=[class(cc)/7 ~(class(cc)/7)];
            x=X(cc,:);
            netj=x*w1';
            y=zeros(size(netj,1),size(netj,2));
            y=1./(1+exp(-netj));
            netk=y*w2';
            z=zeros(size(netk,1),size(netk,2));
            z=1./(1+exp(-netk));
            vals(cc)=norm(t-z);
            if norm(t-z)>0.1
                error=error+1;
            end
        end
        if error==0
            break;
        end
    end
    %}
       
    %norm(t-z)
%     z
%     t
     if norm(t-z)<0.5 
         new_cnt=new_cnt+1;
        if last==1
            counter=counter+1;
        else
            counter=counter+1;
            last=1;
        end
       else
        last=0;
        counter=0;
    end
    maxx=max(maxx,counter);
    if counter>700
        break;
    end
    if new_cnt>floor((5/7)*size(X,1))
        break;
    end
    
end
%{
f= fopen('optdigits.tes');
data = textscan(f,s);
a=data{1};
for i=2:65
    a=[a data{i}];
end
new=a(1,:);
for i=2:size(a,1)
    if mod(a(i,65),7)==0
        new=[new;a(i,:)];
    end
end
%}
new=temp(qw+1:1000,:);

X=[zeros(size(new,1),1)+1 new(:,1:in-1)];
class=new(:,in);
error=0;
vals=zeros(size(X,1),1);
for ind=1:size(X,1)
    t=[class(ind) ~(class(ind))];
    x=X(ind,:);
    netj=x*w1';
    y=zeros(size(netj,1),size(netj,2));
    y=1./(1+exp(-netj));
    netk=y*w2';
    z=zeros(size(netk,1),size(netk,2));
    z=1./(1+exp(-netk));
    if z(1)>z(2)
        z(1)=1;
        z(2)=0;
    end
    if z(2)>z(1)
        z(2)=1;
        z(1)=0;
    end
    vals(ind)=norm(t-z);
    if norm(t-z)>0.1
        error=error+1;
    end
end
100*(1-(error/size(X,1)))
accu(xy)=100*(1-(error/size(X,1)));
xy=xy+1;
end
 save ('accunn.mat','accu');
plot([20:10:900],accu);


end
function [data]=ourdata()
fileID = fopen('data.txt');
% class=
data = textscan(fileID,'%f %f %f %f %f %f %f %f %f %f %f');
fileID = fopen('lables.txt');
class=textscan(fileID,'%f');
% dataset = rdivide(data{1},max(data{1}));
dataset=[];
for i = 2:11
    dataset = horzcat(dataset,rdivide(data{i},max(data{i})));
end
data = horzcat(dataset, class{1});
end








