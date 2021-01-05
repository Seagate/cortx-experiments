#include<iostream>
#include <iterator> 
#include <map> 
#include<queue>
using namespace std;

struct msg
{
	int value;
	int opcode;
};

struct node
{
	map<int, msg> buffer; 

	map<int, node*> pivotmap;
};


map<int, node*> split(node *root)
{map<int, node*> result;
	map<int, node*> ::iterator itr; 
			

			for (itr = root->pivotmap.begin(); itr != root->pivotmap.end();) { 
				node *n = new node;
				result[itr->first]= n;
				
				for(int i=0;i<3 &&  itr != root->pivotmap.end();i++)
			{
				n->pivotmap[itr->first]=itr->second;
				itr++;
			}

			}
			root->pivotmap.clear();
			//root->pivotmap = result;
			//distribute buffer a well//flush buffer to appropriate child and get result add to existing reult if size exceed again split
			return result;
}

map<int, node*> flush(node *root)
{map<int, node*> result;
if(root->pivotmap.size() == 0) //if root buffer full and it is leaf node, split it as b tree and distribute the messages in buffer 
{
	map<int, msg>::iterator itr; 

	for (itr = root->buffer.begin(); itr != root->buffer.end();) { 
		node *n = new node;
		result[itr->first]= n;
		for(int i=0;i<3 && itr != root->buffer.end();i++)
		{
			n->buffer[itr->first] = itr->second;
			itr++;
		}

	}
	root->buffer.clear();
	

}
else 
{
	//find one child and flush ..//later can add timestamp to find situable child
	map<int, node*> ::iterator itr; 
	map<int, msg>::iterator itr2; 
	int max=0,piv=0;

	itr = root->pivotmap.begin();
	int prev = itr->first;
	itr++;

	for (itr2 =  root->buffer.begin(); itr != root->pivotmap.end() && itr2!= root->buffer.end();itr++) { 
		int temp=0;
		while(itr2->first < itr->first && itr2!= root->buffer.end())
		{
			itr2++;
			temp++;

		}
		if(max<temp)
		{
			max = temp;
			piv = prev;

		}
		prev = itr->first;
	}

	int temp=0;
	while(itr2!= root->buffer.end())
	{
		temp++;
		itr2++;
	}
	if(max<temp)
	{
		max = temp;
		piv = prev;
	}
	cout<<"PIV"<<piv<<endl;
	//now flush msg to that child: 

	for (itr2 =  root->buffer.begin(); itr2!= root->buffer.end();itr2++)
	{
		if(itr2->first >= piv)
		{
			for(int i=0;i<max;i++)
			{
				root->pivotmap[piv]->buffer[itr2->first]=itr2->second;
				//clear or delete that buffer item
				root->buffer.erase(itr2++);
				
			}
			break;
		}
	}
	if(root->pivotmap[piv]->buffer.size() <=3)//if buff<size return null
	{
		//cout<<"flush in one of child";
		return result;
	}
	else
	{//if buff exceed size result = flush(child)
		map<int, node*>result_1=flush(root->pivotmap[piv]);
		//add result to pivot of current 
		map<int, node*> ::iterator itr; 
		for (itr =  result_1.begin(); itr != result_1.end();itr++) { 

			root->pivotmap[itr->first] = itr->second;
		}
		result_1.clear();

		//check size exceed  if //exceed split else return result;
		if(root->pivotmap.size() >3)
		{
			
			return split(root);
		}
		//no exceed return null
		
	}





}
return result;
}

node* insert(node *root,int key,int value, int opcode)
{
	if(root == NULL)
	{
		root = new node;
		msg m;
		m.value = value;
		m.opcode =opcode;
		root->buffer[key]=m;
		//root->pivotmap.insert(pair<int, node*>(2,temp));
		return root;
	}else{
		msg m;
		m.value = value;
		m.opcode =opcode;
		root->buffer[key]=m;

	}
	if(root->buffer.size()>3)
	{
		// create new node/root and add pivot if result !=NULL

		map<int, node*>result=flush(root);
		
		if(result.size() != 0)
		{
			root = new node;
			root->pivotmap = result;
		}


	}
	return root;
}

void show(node *root)
{
	queue<node*> g;
	g.push(root);
	while (!g.empty()) {
		node *n = g.front();
		g.pop();
		cout<<"PIVOTS :";
		map<int, node*> ::iterator itr; 
		for (itr = n->pivotmap.begin(); itr != n->pivotmap.end();itr++) { 
			cout<<itr->first<<"  ";
			g.push(itr->second);
		}

		cout<<"BUFFER :";
		map<int, msg> ::iterator itr2; 
		for (itr2 = n->buffer.begin(); itr2 != n->buffer.end();itr2++) { 
			cout<<itr2->first<<"  ";
			cout<<itr2->second.value<<",";
		}
		cout<<endl;

	}
	cout << '\n';
}

int main()
{
	//Consider max pivots per node  =3 pivot pointersand max buffer size =3 messages for this implementation
	int n;
	cout<<"Enter total no. of nodes  : ";
	cin>>n;
	node *root = NULL;
	for(int i=0;i<n;i++)
	{
		int key, value;
		cout<<"Enter key value:";
		cin>>key;

		cin>>value;
		root = insert(root,key,value,0);
		show(root);
	}


}