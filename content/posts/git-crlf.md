---
title: "Git CRLF processing and 'git add --renormalize'"
date: 2022-09-27T15:39:04+08:00
draft: false 
tags: 
    - "c"
    - "git"
---

## git config core.autocrlf


git config core.autocrlf true 


```lang
This does not force normalization of text files, but does ensure that text files that you introduce to the repository have their line endings normalized to LF when they are added, and that files that are already normalized in the repository stay normalized.
```

```shell
git config core.autocrlf false                                                                    
printf "LINEONE\nLINETWO\nLINETHREE" >LF.txt                                                  
printf "LINEONE\r\nLINETWO\r\nLINETHREE" >CRLF.txt
printf "LINEONE\r\nLINETWO\nLINETHREE"   >CRLF_mix_LF.txt
```

Ouput the CRLF.txt:

```shell
cat CRLF.txt  | hexdump -C                                                               
00000000  4c 49 4e 45 4f 4e 45 0d  0a 4c 49 4e 45 54 57 4f  |LINEONE..LINETWO|                                           
00000010  0d 0a 4c 49 4e 45 54 48  52 45 45                 |..LINETHREE|                                                
0000001b 
```

I added some debugging information in git, and let's see these three files
content and object info which storing in git.

```shell
➜  dyrone git:(master) ✗ git add .                                                                                       
[add_to_index] renormalize: ok                                                                                           
[index_path][S_IFREG] path: CRLF.txt, oid:0000000000000000000000000000000000000000                                       
[index_fd] after index fd: oid: 9d953959d3ccf2147bddc3bfcc3ef1d445fdec8e                                                 
[add_to_index] index_path, oid :9d953959d3ccf2147bddc3bfcc3ef1d445fdec8e  is written to odb and set to cached entry      
[add_to_index] renormalize: ok                                                                                           
[index_path][S_IFREG] path: CRLF_mix_LF.txt, oid:0000000000000000000000000000000000000000                                
[index_fd] after index fd: oid: 59a5c42c6e69fbb3a7bde1fee3c72653f41d300a                                                 
[add_to_index] index_path, oid :59a5c42c6e69fbb3a7bde1fee3c72653f41d300a  is written to odb and set to cached entry      
[add_to_index] renormalize: ok                                                                                           
[index_path][S_IFREG] path: LF.txt, oid:0000000000000000000000000000000000000000                                         
[index_fd] after index fd: oid: 27aa24b533b95695aa3b6a64350a6909bdba136d                                                 
[add_to_index] index_path, oid :27aa24b533b95695aa3b6a64350a6909bdba136d  is written to odb and set to cached entry      

➜  dyrone git:(master) ✗ cat .git/index| hexdump -C                                                                      
00000000  44 49 52 43 00 00 00 02  00 00 00 03 63 31 8f 61  |DIRC........c1.a|                                           
00000010  28 bf a6 15 63 31 8f 61  28 bf a6 15 01 00 00 07  |(...c1.a(.......|                                           
00000020  07 06 a0 b1 00 00 81 a4  00 00 01 f5 00 00 00 14  |................|                                           
00000030  00 00 00 1b 9d 95 39 59  d3 cc f2 14 7b dd c3 bf  |......9Y....{...|                                           
00000040  cc 3e f1 d4 45 fd ec 8e  00 08 43 52 4c 46 2e 74  |.>..E.....CRLF.t|                                           
00000050  78 74 00 00 63 31 8f 67  04 3f b3 dc 63 31 8f 67  |xt..c1.g.?..c1.g|                                           
00000060  04 3f b3 dc 01 00 00 07  07 06 a0 c0 00 00 81 a4  |.?..............|                                           
00000070  00 00 01 f5 00 00 00 14  00 00 00 1a 59 a5 c4 2c  |............Y..,|                                           
00000080  6e 69 fb b3 a7 bd e1 fe  e3 c7 26 53 f4 1d 30 0a  |ni........&S..0.|                                           
00000090  00 0f 43 52 4c 46 5f 6d  69 78 5f 4c 46 2e 74 78  |..CRLF_mix_LF.tx|                                           
000000a0  74 00 00 00 63 31 8f 56  02 ab 2e a6 63 31 8f 56  |t...c1.V....c1.V|                                           
000000b0  02 ab 2e a6 01 00 00 07  07 06 a0 90 00 00 81 a4  |................|                                           
000000c0  00 00 01 f5 00 00 00 14  00 00 00 19 27 aa 24 b5  |............'.$.|                                           
000000d0  33 b9 56 95 aa 3b 6a 64  35 0a 69 09 bd ba 13 6d  |3.V..;jd5.i....m|                                           
000000e0  00 06 4c 46 2e 74 78 74  00 00 00 00 08 09 63 33  |..LF.txt......c3|                                           
000000f0  e9 73 e8 e5 be 78 69 a9  f8 32 0c 77 60 be 42 bc  |.s...xi..2.w`.B.|                                           
00000100   
```

We can grab the key informations in above outputs. When we close the config `git
config core.autocrlf`, we can see that there are 3 actually different BLOBs that
be written into INDEX. They are : 

* 9d953959d3ccf2147bddc3bfcc3ef1d445fdec8e
* 59a5c42c6e69fbb3a7bde1fee3c72653f41d300a
* 27aa24b533b95695aa3b6a64350a6909bdba136d

That is because git is not let "autocrlf" happen now, git will record the
original file content as the BLOB, because of the type and number of newlines,
they vary from BLOB to BLOB.

## Attribute "text=auto" 

```shell
echo "*.txt text=auto" >.gitattributes
```

> If you want to ensure that text files that any contributor introduces to the
> repository have their line endings normalized, you can set the text attribute
> to "auto" for all files.
>
> 如果你希望确保写入仓库中的换行符都是经过"规范化的（LF）", 那么你可以将对应的文
> 件类型的attribute设置为“auto”来满足这一点。

我们还可以更加的灵活控制不同文件类型处理换行的不同行为：

```shell
*   text=auto
*.txt		text
*.vcproj	text eol=crlf
*.sh		text eol=lf
*.jpg		-text
```


When we execute the above command "*.txt text=auto" to modify the corresponding
attributes, it is equivalent to requiring git to "normalize (all convert to LF)
the text objects that are subsequently written to the warehouse.

当我们执行了上面的命令"*.txt text=auto"修改了对应的属性后，等同于我们要求git对于
后续写入仓库的文本对象，都进行“规范化（均转化为LF）。


## git add --renormalize

We can use the "--renormalize" parameter of the "add" self-command to
re-"normalize" the text files in the warehouse. For example, in the above
warehouse, among the three files, one is based on CRLF line breaks, and one is
The files are mixed with CRLF and LF, then these two files are actually the
files that need to be "renormalized"

我们可以使用“add” 自命令的“--renormalize” 参数来仓库中文本文件进行重新“规范化”，
例如我们针对上述的仓库中的情况，3个文件中，1个文件为基于CRLF换行，1个文件为CRLF
和LF混用，那么这两个文件实际上就是需要被“renormalized” 的文件。


```shell
➜  dyrone git:(master) ✗ git add --renormalize "*.txt"                                                                                  
[index_path][S_IFREG] path: CRLF.txt, oid:0000000000000000000000000000000000000000                                                      
[index_fd] after index fd: oid: 27aa24b533b95695aa3b6a64350a6909bdba136d                                                                
[add_to_index] index_path, oid :27aa24b533b95695aa3b6a64350a6909bdba136d  is written to odb and set to cached entry                     
[index_path][S_IFREG] path: CRLF_mix_LF.txt, oid:0000000000000000000000000000000000000000                                               
[index_fd] after index fd: oid: 27aa24b533b95695aa3b6a64350a6909bdba136d                                                                
[add_to_index] index_path, oid :27aa24b533b95695aa3b6a64350a6909bdba136d  is written to odb and set to cached entry                     
[index_path][S_IFREG] path: LF.txt, oid:0000000000000000000000000000000000000000                                                        
[index_fd] after index fd: oid: 27aa24b533b95695aa3b6a64350a6909bdba136d                                                                
[add_to_index] index_path, oid :27aa24b533b95695aa3b6a64350a6909bdba136d  is written to odb and set to cached entry                     
➜  dyrone git:(master) ✗ cat .git/index| hexdump -C                                                                                     
00000000  44 49 52 43 00 00 00 02  00 00 00 03 63 31 8f 61  |DIRC........c1.a|                                                          
00000010  28 bf a6 15 63 31 8f 61  28 bf a6 15 01 00 00 07  |(...c1.a(.......|                                                          
00000020  07 06 a0 b1 00 00 81 a4  00 00 01 f5 00 00 00 14  |................|                                                          
00000030  00 00 00 1b 27 aa 24 b5  33 b9 56 95 aa 3b 6a 64  |....'.$.3.V..;jd|                                                          
00000040  35 0a 69 09 bd ba 13 6d  00 08 43 52 4c 46 2e 74  |5.i....m..CRLF.t|                                                          
00000050  78 74 00 00 63 31 8f 67  04 3f b3 dc 63 31 8f 67  |xt..c1.g.?..c1.g|                                                          
00000060  04 3f b3 dc 01 00 00 07  07 06 a0 c0 00 00 81 a4  |.?..............|                                                          
00000070  00 00 01 f5 00 00 00 14  00 00 00 1a 27 aa 24 b5  |............'.$.|                                                          
00000080  33 b9 56 95 aa 3b 6a 64  35 0a 69 09 bd ba 13 6d  |3.V..;jd5.i....m|                                                          
00000090  00 0f 43 52 4c 46 5f 6d  69 78 5f 4c 46 2e 74 78  |..CRLF_mix_LF.tx|                                                          
000000a0  74 00 00 00 63 31 8f 56  02 ab 2e a6 63 31 8f 56  |t...c1.V....c1.V|                                                          
000000b0  02 ab 2e a6 01 00 00 07  07 06 a0 90 00 00 81 a4  |................|                                                          
000000c0  00 00 01 f5 00 00 00 14  00 00 00 19 27 aa 24 b5  |............'.$.|                                                          
000000d0  33 b9 56 95 aa 3b 6a 64  35 0a 69 09 bd ba 13 6d  |3.V..;jd5.i....m|                                                          
000000e0  00 06 4c 46 2e 74 78 74  00 00 00 00 54 52 45 45  |..LF.txt....TREE|                                                          
000000f0  00 00 00 06 00 2d 31 20  30 0a 2c 57 b8 88 a3 06  |.....-1 0.,W....|                                                          
00000100  fb 28 5f 7a 59 5b b6 79  00 18 bc 29 1c 98        |.(_zY[.y...)..|                                             
0000010e  

```

We can see that "--renormalize" re-"normalizes" the txt files in our workspace,
which turns all three files in the repository into LF as newlines. Behind this,
it is actually a two-step operation. The first step is to regenerate a new BLOB
object, and the second step is to write INDEX.

We can see from the output that when the renormalization is completed, the BLOBs
of the three files have become the same object
27aa24b533b95695aa3b6a64350a6909bdba136d, and at this time we can see that the
HASH of the three BLOB objects in INDEX have also been unified to
27aa24b533b95695aa3b6a64350a6909bdba136d .

But it should be noted that although the contents of the three files stored in
the git repository are exactly the same, the filesize of the three files in the
actual INDEX are still different, because the entry in INDEX represents the file
in the workspace and the file in git The mapping between the stored objects,
although the BLOB stored in git is unified after renormalization, the file
stat() stored in the local workspace has not actually changed.

我们可以看到， "--renormalize" 让我们workspace中的txt文件进行重新“规范化”, 这让
仓库中的三个文件全部变为LF作为换行符。这背后，其实是两步的操作，第一步是重新生成
新的BLOB对象，第二步写入INDEX。

我们可以从输出中看到， 当重新规范化执行结束之后，三个文件的BLOB已经变成了同一个
对象27aa24b533b95695aa3b6a64350a6909bdba136d, 而此时我们可以看到INDEX中的三个
BLOB对象的HASH也都已经统一为27aa24b533b95695aa3b6a64350a6909bdba136d.

但是需要注意的一点是，虽然三个文件在git仓库中存储的内容是完全一致，但是实际 上
INDEX中三个文件的filesize还是不同的，因为INDEX中entry代表的是工作空间中的文件与
git中存储的对象之间的映射，虽然renormalize后， git中存储的BLOB得到了统一，但是实
际上存储在本地工作空间中的文件stat()并没有发生变化。
