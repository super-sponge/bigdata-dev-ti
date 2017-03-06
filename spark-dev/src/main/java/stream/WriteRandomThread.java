package stream;

import java.io.*;
import java.net.Socket;

/**
 * Created by sponge on 2017/2/28 0028.
 */
public class WriteRandomThread  extends Thread
{
    Socket clientRequest;// 用户连接的通信套接字
    BufferedReader input;// 输入流
    PrintWriter output;// 输出流

    // serverThread的构造器
    public WriteRandomThread(Socket s)
    {
        this.clientRequest = s;
        // 接收receiveServer传来的套接字
        InputStreamReader reader;
        OutputStreamWriter writer;
        try
        { // 初始化输入、输出流
            reader = new InputStreamReader(clientRequest.getInputStream());
            writer = new OutputStreamWriter(clientRequest.getOutputStream());
            input = new BufferedReader(reader);
            output = new PrintWriter(writer, true);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        output.println("Welcome to the server!");
        // 客户机连接欢迎词
        output.println("Now is: " + new java.util.Date() + " " + "Port:"
                + clientRequest.getLocalPort());
        output.println("What can I do for you?");
        System.out.println("Now is: " + new java.util.Date() + " " + "Port:"
                + clientRequest.getLocalPort());
    }

    @Override
    public void run()
    { // 线程的执行方法

        String command = null; // 用户指令
        String str = null;
        boolean done = false;
        while (true)
        {
            output.println("query this is a word");
            System.out.println("put wod");
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }// end of run
}
