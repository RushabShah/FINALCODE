package com.example.vijayshah.scientificcalculator;

import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.view.View.OnClickListener;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;


public class MainActivity extends AppCompatActivity implements OnClickListener{
    Double mem=0.0;
    TextView display;
    Button one,two,three,four,five,six,seven,eight,nine,zero,dot,open,close,add,sub,mul,div,sin,cos,tan,equal,clear,
            ms,mr,mc;
    String exp="";
    Boolean dec=Boolean.FALSE,opr=Boolean.FALSE;
    String op="0";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {
            display = (TextView) findViewById(R.id.textView);

            one = (Button) findViewById(R.id.one);
            one.setOnClickListener(this);

            two = (Button) findViewById(R.id.two);
            two.setOnClickListener(this);

            three = (Button) findViewById(R.id.three);
            three.setOnClickListener(this);
            //
            four = (Button) findViewById(R.id.four);
            four.setOnClickListener(this);

            five = (Button) findViewById(R.id.five);
            five.setOnClickListener(this);

            six = (Button) findViewById(R.id.six);
            six.setOnClickListener(this);
            //
            seven = (Button) findViewById(R.id.seven);
            seven.setOnClickListener(this);

            eight = (Button) findViewById(R.id.eight);
            eight.setOnClickListener(this);

            nine = (Button) findViewById(R.id.nine);
            nine.setOnClickListener(this);
            //
            zero = (Button) findViewById(R.id.zero);
            zero.setOnClickListener(this);

            open = (Button) findViewById(R.id.open);
            open.setOnClickListener(this);

            close = (Button) findViewById(R.id.close);
            close.setOnClickListener(this);

            dot = (Button) findViewById(R.id.dot);
            dot.setOnClickListener(this);

            add = (Button) findViewById(R.id.add);
            add.setOnClickListener(this);

            mul = (Button) findViewById(R.id.mul);
            mul.setOnClickListener(this);

            div = (Button) findViewById(R.id.div);
            div.setOnClickListener(this);

            sub = (Button) findViewById(R.id.sub);
            sub.setOnClickListener(this);

            clear = (Button) findViewById(R.id.clear);
            clear.setOnClickListener(this);

            ms = (Button) findViewById(R.id.ms);
            ms.setOnClickListener(this);

            mr = (Button) findViewById(R.id.mr);
            mr.setOnClickListener(this);

            mc = (Button) findViewById(R.id.mc);
            mc.setOnClickListener(this);

            equal = (Button) findViewById(R.id.equal);
            equal.setOnClickListener(this);


            sin = (Button) findViewById(R.id.sin);
            sin.setOnClickListener(this);

            cos = (Button) findViewById(R.id.cos);
            cos.setOnClickListener(this);

            tan = (Button) findViewById(R.id.tan);
            tan.setOnClickListener(this);
        }
        catch(NullPointerException e){
            e.printStackTrace();
        }
    }
    @Override
    public void onClick(android.view.View v){
        switch(v.getId()){
            case R.id.one:
                opr=Boolean.FALSE;
                exp+="1";
                display.setText(exp);
                break;

            case R.id.two:
                opr=Boolean.FALSE;
                exp+="2";
                display.setText(exp);
                break;

            case R.id.three:
                opr=Boolean.FALSE;
                exp+="3";
                display.setText(exp);
                break;

            case R.id.four:
                opr=Boolean.FALSE;
                exp+="4";
                display.setText(exp);
                break;
            case R.id.five:
                opr=Boolean.FALSE;
                exp+="5";
                display.setText(exp);
                break;
            case R.id.six:
                opr=Boolean.FALSE;
                exp+="6";
                display.setText(exp);
                break;
            case R.id.seven:
                opr=Boolean.FALSE;
                exp+="7";
                display.setText(exp);
                break;
            case R.id.eight:
                opr=Boolean.FALSE;
                exp+="8";
                display.setText(exp);
                break;
            case R.id.nine:
                opr=Boolean.FALSE;
                exp+="9";
                display.setText(exp);
                break;
            case R.id.zero:
                opr=Boolean.FALSE;
                exp+="0";
                display.setText(exp);
                break;

            case R.id.open:
                exp+="(";
                display.setText(exp);
                break;

            case R.id.close:
                exp+=")";
                display.setText(exp);
                break;

            case R.id.dot:
                if(!dec){
                    opr=Boolean.FALSE;
                    dec=Boolean.TRUE;
                    exp+=".";
                    display.setText(exp);
                    break;
                }
                else{
                    Toast.makeText(getApplicationContext(),"Cannot add another decimal",Toast.LENGTH_LONG).show();
                    break;
                }

            case R.id.add:
                if(!opr){
                    dec=Boolean.FALSE;
                    opr=Boolean.TRUE;
                    exp+="+";
                    op="+";
                    display.setText(exp);
                    break;
                }
                else{
                    Toast.makeText(getApplicationContext(),"Cannot add another operator",Toast.LENGTH_LONG).show();
                    break;
                }
            case R.id.sub:
                if(!opr){
                    dec=Boolean.FALSE;
                    opr=Boolean.TRUE;
                    exp+="-";
                    op="-";
                    display.setText(exp);
                    break;
                }
                else{
                    Toast.makeText(getApplicationContext(),"Cannot add another operator",Toast.LENGTH_LONG).show();
                    break;
                }

            case R.id.div:
                if(!opr){
                    dec=Boolean.FALSE;
                    opr=Boolean.TRUE;
                    exp+="/";
                    op="/";
                    display.setText(exp);
                    break;
                }
                else{
                    Toast.makeText(getApplicationContext(),"Cannot add another operator",Toast.LENGTH_LONG).show();
                    break;
                }

            case R.id.mul:
                if(!opr){
                    dec=Boolean.FALSE;
                    opr=Boolean.TRUE;
                    exp+="*";
                    op="*";
                    display.setText(exp);
                    break;
                }
                else{
                    Toast.makeText(getApplicationContext(),"Cannot add another operator",Toast.LENGTH_LONG).show();
                    break;
                }
            case R.id.equal:
                calculate();
                break;
            case R.id.clear:
                exp="";
                dec=Boolean.FALSE;
                opr=Boolean.FALSE;
                op="0";
                display.setText(exp);
                break;
            case R.id.ms:
                mem=Double.parseDouble(display.getText().toString());
                break;
            case R.id.mr:
                exp=exp+mem;
                display.setText(exp);
                break;
            case R.id.mc:
                mem=0.0;
                display.setText("Memory Cleared");
                break;
            case R.id.sin:
                writeToFile(display.getText().toString(),getApplicationContext());
                break;
            case R.id.cos:
                display.setText(readFromFile(getApplicationContext()));
                break;
        }
    }

    private void writeToFile(String data,Context context){
        try{
            OutputStreamWriter osw=new OutputStreamWriter(context.openFileOutput("hello.txt",context.MODE_PRIVATE));
            osw.write(data);
            osw.close();
        }
        catch (Exception e){
            Log.e("Exception",e.toString());
        }
    }

    private String readFromFile(Context context){
        String ret="";
        try{
            InputStream is=getAssets().open("hi.txt");
            if(is!=null){
                InputStreamReader isr=new InputStreamReader(is);
                BufferedReader br=new BufferedReader(isr);
                StringBuilder sb=new StringBuilder();
                String r="";
                while((r=br.readLine())!=null){
                    sb.append(r);
                }
                is.close();
                ret=sb.toString();
            }
        }
        catch (Exception f){
            Log.e("Exception",f.toString());
        }
        return ret;
    }

    public void calculate(){
        display.setText("");
        exp=""+EvaluateString.Evaluate(exp);
        display.setText(exp);
    }
}
