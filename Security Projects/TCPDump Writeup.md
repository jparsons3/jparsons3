![image](https://github.com/jparsons3/jparsons3/assets/142419088/1fa17ce0-9b95-4850-b0df-54814d44e112)# TCPDump Writeup

# What is TCPDump?

> TCPDump is a command that allows us to look at packets that are sent and received on a host device or a Packet Captured File (PCAP). This can also be used to filter and analyze data.

> TCPDump is a command-line tool that allows users to intercept and analyze network traffic in real-time. It can be used to capture packets sent and received on a host device or a Packet Captured File (PCAP).

In addition to capturing packets, TCPDump also provides options to filter and analyze captured data. Some of the filtering options include filtering by protocol, source or destination IP address, port number, and many more. TCPDump can also be used with other tools such as Wireshark to provide a more detailed analysis of captured packets.

The filter for this... is host.

$ `tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52`

For this command we are telling tcpdump to not resolve hostnames (-n) and we are telling it to read in the data from a file (-r). we are also taking a look at the network traffic for the designated host on all incoming and outgoing ports. 

![image](https://github.com/jparsons3/jparsons3/assets/142419088/9993db00-b47e-4908-86a9-f30159b81fdb)


## what exactly is the image above showing us?
```
                    TCPDUMP FLAGS
Unskilled =  URG  =  (Not Displayed in Flag Field, Displayed elsewhere)
Attackers =  ACK  =  (Not Displayed in Flag Field, Displayed elsewhere)
Pester    =  PSH  =  [P] (Push Data)
Real      =  RST  =  [R] (Reset Connection)
Security  =  SYN  =  [S] (Start Connection)
Folks     =  FIN  =  [F] (Finish Connection)
          SYN-ACK =  [S.] (SynAcK Packet)
                     [.] (No Flag Set/ ACK in reality for this writeup) 
```


- we are seeing the timestamps for each of the packets timestamps.
    - timestamp
    
    ![image](https://github.com/jparsons3/jparsons3/assets/142419088/b1dc5917-eb34-4f21-944e-7cec63e30223)

    
    - protocols
    
    ![image](https://github.com/jparsons3/jparsons3/assets/142419088/f83a89f3-50ce-4cb4-bf11-5ad8324c8e6e)

    - source IP and destination IP
    ![image](https://github.com/jparsons3/jparsons3/assets/142419088/15508036-6d5f-4f8a-8aca-d8751dbc9687)

    
    - Flags and sequences and leng
    ![image](https://github.com/jparsons3/jparsons3/assets/142419088/87ff8ed4-949e-43d8-81d6-368aa8e88c2b)

  
    ## we can now make the filtering more fine tuned. lets add a port number
    
    `tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52 and port 80`
    
    ![image](https://github.com/jparsons3/jparsons3/assets/142419088/4ebebe58-3a60-4223-95fd-8815c3d2c0f3)

    
    with the added port number, we can now see all the packets received on port 80.
    
    We can also look at the packets in Ascii decoded. 
    $`tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52 and port 80 -A`
    
    ![https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-23-36.png](https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-23-36.png)
    
    As you can see above, we now can see the actual http GET requests and the responses.
    
    - Lets look at the timestamp: 08:
        
        14:32.638976
        
        ![https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-24-48.png](https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-24-48.png)
        
        - We can now see that powershell was used to commence the attack here!
        
        ![image](https://github.com/jparsons3/jparsons3/assets/142419088/ea775f39-3ae7-4eb5-8fca-97017f15c3d9)

        
        - Here is the Hex version of the timestamp  with the attack as well with the x flag if you want to see this in hex.
        
        `tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52 and port 80 -AX`
        
        ![image](https://github.com/jparsons3/jparsons3/assets/142419088/5d263650-aeaf-4d21-b976-3821d1152d5c)

        
        We can specify protocols like ipv6
        
        $ `tcpdump -n -r magnitude_1hr.pcap ip6`
        
        we can also specify network rangers to see tracking going to or leaving from a RANGE of IP addresses. for example this will help us answer questions like “are there any other systems talking to this IP range? 
        $`tcpdump -n -r magnitude_1hr.pcap net 192.168.99.0/24`
