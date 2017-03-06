package stream;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Date;

/**
 * Created by sponge on 2017/2/28 0028.
 */
public class ReceiveServer {
    final int RECEIVE_PORT = 9090;// 该服务器的端口号

    // receiveServer的构造器
    public ReceiveServer()
    {
        ServerSocket rServer = null;// ServerSocket的实例
        Socket request = null; // 用户请求的套接字
        Thread receiveThread = null;
        try
        {
            rServer = new ServerSocket(RECEIVE_PORT);
            // 初始化ServerSocket
            System.out.println("Welcome to the server!");
            System.out.println(new Date());
            System.out.println("The server is ready!");
            System.out.println("Port: " + RECEIVE_PORT);
            while (true)
            {
                // 等待用户请求
                request = rServer.accept();

                // 接收客户机连接请求
//                receiveThread = new serverThread(request);
                receiveThread = new WriteRandomThread(request);
                // 生成serverThread的实例
                receiveThread.start();
                // 启动serverThread线程
            }
        } catch (IOException e)
        {
            System.out.println(e.getMessage());
        }
    }

    public static void main(String args[])
    {
        new ReceiveServer();
    } // end of main
} // end of class