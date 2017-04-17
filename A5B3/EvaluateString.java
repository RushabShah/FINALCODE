package com.example.vijayshah.scientificcalculator;

import java.util.Stack;

/**
 * Created by vijay shah on 14-04-2017.
 */

public class EvaluateString {
    public static Double Evaluate(String exp){
        char[] tokens=exp.toCharArray();
        Stack<Double> values=new Stack<>();
        Stack<Character> ops=new Stack<>();
        for(int i=0;i<tokens.length;i++){
            if((tokens[i]>='0' && tokens[i]<='9')||tokens[i]=='.'){
                int j=i;
                StringBuffer sbuf=new StringBuffer();
                while((j<tokens.length)&&((tokens[j]>='0' && tokens[j]<='9')||tokens[j]=='.')){
                    sbuf.append(tokens[j]);
                    if(j>i){
                        i=j;
                    }
                    j+=1;
                }

                values.push(Double.parseDouble(sbuf.toString()));
            }
            else if(tokens[i]=='('){
                ops.push(tokens[i]);
            }
            else if(tokens[i]==')'){
                while(ops.peek()!='('){
                    values.push(applyOp(ops.pop(),values.pop(),values.pop()));
                }
                if(ops.peek()=='('){
                    ops.pop();
                }
            }
            else if(tokens[i]=='+' ||tokens[i]=='-' ||tokens[i]=='*' ||tokens[i]=='/'){
                while((!ops.empty()) && hasPrecedence(tokens[i],ops.peek())){
                    values.push(applyOp(ops.pop(),values.pop(),values.pop()));
                }
                ops.push(tokens[i]);
            }
        }
        while (!ops.empty()){
            values.push(applyOp(ops.pop(),values.pop(),values.pop()));
        }
        return values.pop();
    }

    public static Boolean hasPrecedence(char op1,char op2){
        if( op2=='(' || op2==')'){
            return Boolean.FALSE;
        }
        else if((op1=='/'||op1=='*')&&(op2=='+'||op2=='-')){
            return Boolean.FALSE;
        }
        return Boolean.TRUE;
    }

    public static Double applyOp(char op,Double b, Double a){
        switch (op){
            case '+':
                return a+b;
            case '-':
                return a-b;
            case '*':
                return a*b;
            case '/':
                if(b!=0){
                    return a/b;
                }
                else{
                    throw new UnsupportedOperationException("Cannot Divide by Zero");
                }
        }
        return 0.0;
    }
}
