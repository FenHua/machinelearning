function W = reliefF(Dnolabel,Dlabel,Num,k,typeD,Topn) 
%      
%      用reliefF完成特征排列       
%      Dlabel 是每一个结果有标记数组        
%      Dlabel中的数据以1，2，3等形式显示
%      Dnolabel是每个结果没有标记的数组         
%      Num 是随机选择实例循环的次数             
%      k 是没有选中的最近命中的数量
%      Weight用于输出，它代表每一个属性的等级
%     typeD 是Dnolabel的类型,如果它是数字的,   typeD=0;   
%     如果它是正常的属性, typeD=1; 
%
[y,x]=size(Dnolabel);  
W = zeros(1,Topn); 
%计算有标记的可能性 
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
%循环随机选择实例  
for NumN=1:Num     
    NumN      
    %随机选择一个实例
    InstanceId = round([y.*rand(1)]);     
    while InstanceId==0,          
        InstanceId = round([y.*rand(1)]);     
    end      
    index = 1;      
    %计算被选择的实例和其它实例之间的距离
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
     %按升序的格式排列距离
     DistanceArray=sortrows(DistanceArray,1);           
     Result=zeros(LabelRange,y);     
     classSize = zeros(1,LabelRange);     
     for i=1:y-1          
         class = Dlabel(DistanceArray(i,2));              
         classSize(class) = classSize(class)+1;          
         Result(class,classSize(class))=DistanceArray(i,2);     
     end
      %操作每一个实例        
      MissW=0; 
      %初始化部分相关但是丢弃的值
      HitW=0; %t初始化部分相关并且命中的值    
      for AttributeNum=1:x          
          %计算属性中最大最小值的差        
          diff = Weight(AttributeNum,1);          
          if (dominoDiff(AttributeNum)<0.0000001)             
              Weight(AttributeNum,1)=0;              
              Weight(AttributeNum,2)=AttributeNum;             
              continue;         
          end
           %计算每一个属性的权值                
           for i=1:k 
               %k是被选中的最近邻居的数量
               idHit = Result(Dlabel(InstanceId),k );             
               %命中              
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
                   %遗弃 
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