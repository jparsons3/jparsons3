# Memory Analysis with Volatility3

- Memory Analysis Video with Volatility3 explained by John Strand in the video below
    
    [(137) AASLR: Volatility3 is awesome! | John Strand - YouTube](https://www.youtube.com/watch?v=9M3aWrbziBg&list=PLDEie_Pi1bGYiNiTKcFx-cBzddh1OAk1N&index=7&t=1073s&ab_channel=AntisyphonTraining)
    
    [https://www.youtube.com/watch?v=9M3aWrbziBg&list=PLDEie_Pi1bGYiNiTKcFx-cBzddh1OAk1N&index=7&t=1073s&ab_channel=AntisyphonTraining](https://www.youtube.com/watch?v=9M3aWrbziBg&list=PLDEie_Pi1bGYiNiTKcFx-cBzddh1OAk1N&index=7&t=1073s&ab_channel=AntisyphonTraining)
    

## What is Memory Analysis?

Memory Analysis is taking a machine that was attacked through a vulnerability, malware, exploit or any other attacking method, and taking the information that is placed in memory and finding out what prompted the attack to be successful. 

<aside>
📥 From the resources of the video, this is not working on a live machine as it was taken from a virtual snapshot of the machine. You can get memory dumps of any machine. (Ex: [Configure memory dump files for Server Core installation | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/server-core/server-core-memory-dump), [Configuring a Windows server to produce a memory dump file | Dell US](https://www.dell.com/support/kbdoc/en-us/000141638/configuring-a-windows-server-to-produce-a-memory-dump-file)) Also, this will be following a guide as if you have already downloaded volatility and the memdump in the VMware Lab. (its a .VMEM file)

</aside>

> This way with a memory dump of the machine, you do not have to interact with the attacker or the vulnerable machine live as the memory dump is taken at the specified point in memory
> 

## How to begin Memory Analysis in Linux (ubuntu)

Login and password to VM in VMware is PW:adhd

1. Extract the Memdump & volatility
    - setup volatility and the memdump
        
        Now, select the volatility_2.6_win64_standalone directory:
        
        ![https://github.com/strandjs/IntroLabs/raw/master/IntroClassFiles/Tools/IntroClass/Memory/attachments/Clipboard_2020-12-09-14-11-23.png](https://github.com/strandjs/IntroLabs/raw/master/IntroClassFiles/Tools/IntroClass/Memory/attachments/Clipboard_2020-12-09-14-11-23.png)
        
        Next, right click on the memdump file and then select 7-Zip and then Extract Here. Please note that the file name does not end with 7z on the left display column. However, on the far right column you can see it is a 7Z file. extract it:
        
        ![https://github.com/strandjs/IntroLabs/raw/master/IntroClassFiles/Tools/IntroClass/Memory/attachments/Clipboard_2020-12-09-14-12-09.png](https://github.com/strandjs/IntroLabs/raw/master/IntroClassFiles/Tools/IntroClass/Memory/attachments/Clipboard_2020-12-09-14-12-09.png)
        
        Now we need to extract Volatility in the Terminal. Open up the Terminal and run the following command:
        
        ```
        cd /mnt/c/IntroLabs/ 
        tar xvfz ./volatility3-1.0.0.tar.gz
        cd volatility3-1.0.0/
        ```
        

<aside>
📥 What is volatility? [Volatility 3 — Volatility 3 2.4.2 documentation](https://volatility3.readthedocs.io/en/latest/)

</aside>

1. Running volatility and checking the network connections. 
    - Run volatility to take a look at the memdump’s network connection.
        
        ```c
        windows
        python3 vol.py -f /mnt/c/tools/volatility_2.6_win64_standalone/memdump.vmem windows.netscan
        OR (linux)
        python3 vol. -f /mnt/c/tools/volatility_2.6_win64_standalone/memdump.vmem netscan
        
        ```
                
        ---
        
                    
            ```c
            python3 vol.py -f /mnt/c/tools/volatility_2.6_win64_standalone/memdump.vmem windows.pslist
            
            ```
                       
        
        > Port 445 Server Message Block ([SMB](https://www.notion.so/Network-Ports-a6c11047a76843d79e70d2e7749e236b?pvs=21)) is being used to connect to other workstations. ****This raises some red flags.**** SMB should only be getting used for ****servers to communicate with workstations**!** Not workstations directly communicating with each other.
        > 
        
        we can now see that the attacked machine (192.168.192.145) had an established connection to the attacker machine (192.168.192.146). the PID 4 is the system process.  
        
        > the system process is running net.exe or conhost.exe (we will see in a moment). Thankfully with volatility3, right below that, we can see that the PID for the software ‘Trustme.exe’ we can see that the PID for said process is 5452.
        > 
        
        <aside>
        ✂️ Why is the process coming back as closed? 
        
        The process is coming back as closed since the interpreter processes these services that way. (might be every 30 minutes it reestablishes that connection. so it could be seen multiple times throughout certain intervals.)  even if the connection is dead, its still logged in the dump for a while.
        
        </aside>
        
2. Running volatility and checking the processes that are being used in the dump 
    - Running PSlist (Process List)
        
        > it is critical to do live forensics on a system to see specifically what services are being run through SVChost.exe. many SVChost came up during the forensics of the device. the command to see the services is ‘tasklist /SVC’ to see what the services are. ************************************See bottom of this page to see how to check services offline in a dump************************************
        > 
        
        
        There are more services than what is being offered in the screenshot above. 
        
        1. according to the pslist in the dump file, the process ‘TrustMe.exe’ has the PPID 3616 which is the windows explorer application. this tells us that the application was double clicked and ran. 
            - chrome was double clicked and ran
            - someone went to the website, downloaded the exe and ran trustme.exe
        
        | PID | PPID | Imagefilename | Offset | Threads/Handles/SessionId |
        | --- | --- | --- | --- | --- |
        
        b. right below trustme.exe, we can also see that CMD and net.exe was invoked by the PPID trustme.exe. this is the system making a connection.
        
        ---
        
        - Another way to see this information is using windows.pstree to see the process hierarchy. chrome was run by explorer, then trustme.exe was downlaoded an ran through explorer. trustme then invoked the processes cmd which invoked conhost and net.exe
            
            
    - [Dynamic link libraries](https://www.notion.so/Memory-Analysis-Dictionary-References-e7a0b7acd4c740ad8a9906a2c7c10fba?pvs=21) are seen and run to see what DLL’s are being run with the process.
        
        ```bash
        python3 vol.py -f /mnt/c/tools/volatility_2.6_win64_standalone/memdump.vmem dlllist --pid 5452
        ```
        
        ```bash
        Volatility 3 Framework 1.0.0
        Progress:  100.00               PDB scanning finished
        PID     Process Base    Size    Name    Path    LoadTime        File output
        
        5452    TrustMe.exe     0x400000        0x16000 TrustMe.exe     C:\Users\Sec504\Downloads\TrustMe.exe   2020-11-30 17:43:17.000000      Disabled
        5452    TrustMe.exe     0x7ffaf6290000  0x1d1000        -       -       2020-11-30 17:43:17.000000      Disabled
        5452    TrustMe.exe     0x594e0000      0x52000 wow64.dll       C:\Windows\System32\wow64.dll   2020-11-30 17:43:17.000000      Disabled
        5452    TrustMe.exe     0x59540000      0x77000 wow64win.dll    C:\Windows\System32\wow64win.dll        2020-11-30 17:43:17.000000      Disabled
        5452    TrustMe.exe     0x594d0000      0xa000  wow64cpu.dll    C:\Windows\System32\wow64cpu.dll        2020-11-30 17:43:17.000000
        ```
        
        > Here we can see the dll’s associated with the trustme processes
        > 
3. Running volatility and using Malfind
    - To be able to run Malfind with volatility to check if the process is really running any suspicious activities.
        
        ```bash
        python3 vol.py -f /mnt/c/tools/volatility_2.6_win64_standalone/memdump.vmem windows.malfind.Malfind
        ```
        
        Malfind lit up the trustme application saying that something has been injected into the software three times

        

## How would you check the SVChost info in a offline memory dump?

1. You might want to do it to find the DLL’s. take the process id and run the DLL list for the PID for the specific .exe.
    1. for the example below we are going to look at the process 1180
    
    ```bash
    python3 vol.py -f /mnt/c/tools/volatility_2.6_win64_standalone/memdump.vmem dlllist --pid 1180
    ```
    

in this case the svchost that was chosen was loading legit DLL’s. 


<aside>
💡 Something about SVChost in general, it will **************Listen************** to ports all the time but it is strange to see SVChosts making outbound connections


</aside>

## What is the best way to go through processes and making sure they’re safe?

we dont not want to do that. if we were to do that, it would take way too long looking at the currently running exe’s on a live machine!


1. Its best to start with looking at the network to see if there are any established connections relating to malware on the system
    1. you can run Netstat to gather that information 

    
    ```bash
    netstat -naob
    ```
    
    with netstat you can now see that there is an established connection on the live machine and then you can begin to work from there. 
    

## Reference point

[Memory Analysis Dictionary References](https://www.notion.so/Memory-Analysis-Dictionary-References-e7a0b7acd4c740ad8a9906a2c7c10fba?pvs=21)
