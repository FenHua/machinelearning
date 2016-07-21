function W = reliefF(Dnolabel,Dlabel,Num,k,typeD,Topn) 
%      
%      ��reliefF�����������       
%      Dlabel ��ÿһ������б������        
%      Dlabel�е�������1��2��3����ʽ��ʾ
%      Dnolabel��ÿ�����û�б�ǵ�����         
%      Num �����ѡ��ʵ��ѭ���Ĵ���             
%      k ��û��ѡ�е�������е�����
%      Weight���������������ÿһ�����Եĵȼ�
%     typeD ��Dnolabel������,����������ֵ�,   typeD=0;   
%     �����������������, typeD=1; 
%
[y,x]=size(Dnolabel);  
W = zeros(1,Topn); 
%�����б�ǵĿ����� 
LabelRange=max(Dlabel)-min(Dlabel)+1; 
LabelCount=zeros(1,LabelRange); 
LabelP=zeros(1,LabelRange);
for i=1:y      
    LabelCount(Dlabel(i))=LabelCount(Dlabel(i))+1;    
end  
for j=1:LabelRange      
    LabelP(j)=LabelCount(j)/y; 
end 
LabelP
%*********************************************    
DistanceArray=zeros(y-1,2); 
%Weight=zeros(1,x); 
Weight=zeros(x,2); 
Diff=0; 
for i=1:x      
    dominoDiff(i) = max(Dnolabel(:,i))- min(Dnolabel(:,i));
end
%ѭ�����ѡ��ʵ��  
for NumN=1:Num     
    NumN      
    %���ѡ��һ��ʵ��
    InstanceId = round([y.*rand(1)]);     
    while InstanceId==0,          
        InstanceId = round([y.*rand(1)]);     
    end      
    index = 1;      
    %���㱻ѡ���ʵ��������ʵ��֮��ľ���
     for i=1:y          
         if (i~=InstanceId)             
             for j=1:x                  
                 DistanceArray(index,1)=DistanceArray(index,1)+...                     
                     (Dnolabel(i,j)-Dnolabel(InstanceId,j))^2;             
             end              
             DistanceArray(index,1)=(DistanceArray(index,1)/x)^(0.5); 
             DistanceArray(index,2)=i;             
             index = index+1;         
         end     
     end      
     %������ĸ�ʽ���о���
     DistanceArray=sortrows(DistanceArray,1);           
     Result=zeros(LabelRange,y);     
     classSize = zeros(1,LabelRange);     
     for i=1:y-1          
         class = Dlabel(DistanceArray(i,2));              
         classSize(class) = classSize(class)+1;          
         Result(class,classSize(class))=DistanceArray(i,2);     
     end
      %����ÿһ��ʵ��        
      MissW=0; 
      %��ʼ��������ص��Ƕ�����ֵ
      HitW=0; %t��ʼ��������ز������е�ֵ    
      for AttributeNum=1:x          
          %���������������Сֵ�Ĳ�        
          diff = Weight(AttributeNum,1);          
          if (dominoDiff(AttributeNum)<0.0000001)             
              Weight(AttributeNum,1)=0;              
              Weight(AttributeNum,2)=AttributeNum;             
              continue;         
          end
           %����ÿһ�����Ե�Ȩֵ                
           for i=1:k 
               %k�Ǳ�ѡ�е�����ھӵ�����
               idHit = Result(Dlabel(InstanceId),k );             
               %����              
               if(round(typeD)==0)                  
                   diff = diff - abs( Dnolabel(idHit, AttributeNum) -...                     
                       Dnolabel(InstanceId, AttributeNum) )...                     
                       /dominoDiff(AttributeNum)/k;              
               else                  
                   if (round(Dnolabel(InstanceId,AttributeNum))...                         
                           ==round(Dnolabel(idHit, AttributeNum)))                     
                       diff=diff-0;                 
                   else                      
                       diff=diff-1;                 
                   end             
               end
           end
           for c=1:LabelRange             
               if (c==Dlabel(InstanceId))                 
                   continue;            
               end                           
               P=LabelP(c)/(1-LabelP(Dlabel(InstanceId)));             
               for i=1:k                  
                   idMiss = Result(c,i);                 
                   %���� 
                    if (round(typeD)==0)                      
                        diff = diff + P*abs( Dnolabel(idMiss, AttributeNum) -...                         
                            Dnolabel(InstanceId, AttributeNum) )...                         
                            /dominoDiff(AttributeNum)/k;                  
                    else                      
                        if (round(Dnolabel(InstanceId,AttributeNum))...                             
                                ==round(Dnolabel(idHit, AttributeNum)))                         
                            diff=diff;                     
                        else                          
                            diff=diff+1;
                        end                 
                    end               
               end          
           end % for m=1:LabelRange         
           Weight(AttributeNum,1)=diff;          
           Weight(AttributeNum,2)=AttributeNum;     
      end 
      %  for AttributeNum=1:x 
end % for NumN=1:Num   
Weight(AttributeNum,1)=diff/Num;  
Weight(AttributeNum,2)=AttributeNum;         
W1 = sortrows(Weight); 
for i = 1:Topn      
    W(i) = W1(x-i+1,2); 
end      