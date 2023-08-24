# TCPDump Writeup

# What is TCPDump?

> TCPDump is a command that allows us to look at packets that are sent and received on a host device or a Packet Captured File (PCAP). This can also be used to filter and analyze data which includes
> 

TCPDump is a command-line tool that allows users to intercept and analyze network traffic in real-time. It can be used to capture packets sent and received on a host device or a Packet Captured File (PCAP).

In addition to capturing packets, TCPDump also provides options to filter and analyze captured data. Some of the filtering options include filtering by protocol, source or destination IP address, port number, and many more. TCPDump can also be used with other tools such as Wireshark to provide a more detailed analysis of captured packets.

The filter for this... is host.

$ `tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52`

For this command we are telling tcpdump to not resolve hostnames (-n) and we are telling it to read in the data from a file (-r). we are also taking a look at the network traffic for the designated host on all incoming and outgoing ports. 

![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled.png)

## what exactly is the image above showing us?

- we are seeing the timestamps for each of the packets timestamps.
    - timestamp
    
    ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%201.png)
    
    - protocols
    
    ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%202.png)
    
    - source IP and destination IP
    
    ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%203.png)
    
    - Flags and sequences and leng
    
    ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%204.png)
    
    ## we can now make the filtering more fine tuned. lets add a port number
    
    `tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52 and port 80`
    
    ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%205.png)
    
    with the added port number, we can now see all the packets received on port 80.
    
    We can also look at the packets in Ascii decoded. 
    $`tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52 and port 80 -A`
    
    ![https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-23-36.png](https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-23-36.png)
    
    As you can see above, we now can see the actual http GET requests and the responses.
    
    - Lets look at the timestamp: 08:
        
        14:32.638976
        
        ![https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-24-48.png](https://github.com/strandjs/ClassLabs/raw/main/Tools/IntroClass/TCPDump/attachments/Clipboard_2020-12-09-18-24-48.png)
        
        - We can now see that powershell was used to commence the attack here!
        
        ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%206.png)
        
        - Here is the Hex version of the timestamp  with the attack as well with the x flag if you want to see this in hex.
        
        `tcpdump -n -r magnitude_1hr.pcap host 192.168.99.52 and port 80 -AX`
        
        ![Untitled](TCPDump%20Writeup%20d9f7c25f24184fc899c889cf399942cd/Untitled%207.png)
        
        We can specify protocols like ipv6
        
        $ `tcpdump -n -r magnitude_1hr.pcap ip6`
        
        we can also specify network rangers to see tracking going to or leaving from a RANGE of IP addresses. for example this will help us answer questions like “are there any other systems talking to this IP range? 
        $`tcpdump -n -r magnitude_1hr.pcap net 192.168.99.0/24`