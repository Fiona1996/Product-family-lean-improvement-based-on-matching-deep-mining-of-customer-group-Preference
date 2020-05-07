% �ṹͻ��Ľ�ģ�����
% ���Ŷ���Ϊ��̬��ǰ���������ַ���������֤�����ַ��������Ľ����ͬ
% �췽��������û�и������δ�����

%% �����Ա����������,���ݱ������������С��
files = 'D:\Files\����\2-NewVersion\2-��һ������\6-data-cluster2-price.xlsx';
sheet1='cluster1';
sheet2='cluster2';
sheet3='aggregate';
sheet4='chowreg1';
sheet5='model1';
sheet6='model2';
variables1=xlsread(files,sheet1);
variables2=xlsread(files,sheet2);
variables1 = variables1(:, 2:size(variables1,2));
variables2 = variables2(:, 2:size(variables2,2));
variables=[variables1;variables2];
[n1,K1]=size(variables1); % n����������������K�������������
[n2,K2]=size(variables2); % n����������������K�������������
x1=[ones(n1,1),variables1(:,2:K1)]; % �Ա���
y1=variables1(:,1);        
[n2,K2]=size(variables2); % n����������������K�������������
x2=[ones(n2,1),variables2(:,2:K2)]; % �Ա���
y2=variables2(:,1);
x=[x1;x2];
y=[y1;y2];
n=n1+n2; % ����������
% JΪԼ������(��һ���ɶ�)��NΪ�ڶ����ɶ�
J=K2;
N=n1+n2-K1-K2;

%% ����1��P118��P83�����������ع鷽��ϵ����ͬ�ļ���
% b1=(x1'*x1)\x1'*y1; % ϵ��
% b2=(x2'*x2)\x2'*y2;
% e1=y1-x1*b1; % �в�
% e2=y2-x2*b2;
files = 'D:\Files\����\2-NewVersion\2-��һ������\10-structural.xlsx';
[b1,T_P1,s21,e1,R21,adjustR21,rF1,F_P_model1]=LinearRegression(variables1,files,sheet5);
[b2,T_P2,s22,e2,R22,adjustR22,rF2,F_P_model2]=LinearRegression(variables2,files,sheet6);
R=[eye(K2),-1*eye(K2)]; % Լ������,J=K2(x2������)
q=zeros(K2,1); % Լ������
baggregate=[b1;b2];
ssebefore=e1'*e1;
sseafter=e2'*e2;
sse=e1'*e1+e2'*e2;
s2=sse/(N); % ����������ɶ�Ϊn1+n2-K1-K2
xnew=[x1,zeros(n1,K2);zeros(n2,K1),x2]; % P118��������µ�x
F1=((R*baggregate-q)'/(R/(xnew'*xnew)*R')*(R*baggregate-q))/(s2*J);
F1_P=1-fcdf(F1,J,N);

%% ����2��P118��P87������һ���ع鷽�̵ļ��飬��Լ��
% ��Լ�������Իع鲻��ʹ����Լ�����Իع�Ľ������Ҫ���¼��㣨���ɶȲ�ͬ��
[b,T_P,~,estar,R2,adjustR2,rF,F_P_model]=LinearRegression(variables,files,sheet3); 
ssestar=estar'*estar;
F2=(ssestar-sse)*(N)/(J*sse);
F2_P=1-fcdf(F2,J,N);

%% �췽������������ֲ��������ֲ�
V1=ssebefore/(n1-K1)./(x1'*x1); % s2����������
V2=sseafter/(n2-K2)./(x2'*x2);
Wald1=(b1-b2)'/(V1+V2)*(b1-b2);

Wald1_P=1-chi2cdf(Wald1,J);
Wald2=N*(ssestar/sse-1);
Wald2_P=1-chi2cdf(Wald2,J);
LM=n*J/(N/F1+J);
LM_P=1-chi2cdf(Wald2,J);

%% �ṹͻ�������д��
results1=[b,T_P,b1,T_P1,b2,T_P2];
results21=[R2;adjustR2;n;ssestar;rF;F_P_model];
results22=[R21;adjustR21;n1;ssebefore;rF1;F_P_model1];
results23=[R22;adjustR22;n2;sseafter;rF2;F_P_model2];
results3=[F1,F1_P;F2,F2_P;Wald1,Wald1_P;Wald2,Wald2_P;LM,LM_P];
xlswrite(files,results1,sheet4,'B4');
xlswrite(files,results21,sheet4,'C14');
xlswrite(files,results22,sheet4,'E14');
xlswrite(files,results23,sheet4,'G14');
xlswrite(files,results3,sheet4,'J4');

