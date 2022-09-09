# WRK 压力测试工具

Github: https://github.com/wg/wrk

## 1. 安装

克隆：

```shell
git clone https://github.com/wg/wrk
```

> 目录结构：（2022-09-07）
> ```shell
> root@ip-10-100-7-107:~/wrk# ll
> total 4372
> -rw-r--r--  1 root root       9 Sep  7 07:03 .gitignore
> -rw-r--r--  1 root root     945 Sep  7 07:03 CHANGES
> -rw-r--r--  1 root root     916 Sep  7 07:03 INSTALL
> -rw-r--r--  1 root root   10489 Sep  7 07:03 LICENSE
> -rw-r--r--  1 root root    2674 Sep  7 07:03 Makefile
> -rw-r--r--  1 root root    5420 Sep  7 07:03 NOTICE
> -rw-r--r--  1 root root    3497 Sep  7 07:03 README.md
> -rw-r--r--  1 root root    4158 Sep  7 07:03 SCRIPTING
> drwxr-xr-x  2 root root    4096 Sep  7 07:03 deps/
> drwxr-xr-x  8 root root    4096 Sep  7 07:13 obj/
> drwxr-xr-x  2 root root    4096 Sep  7 07:03 scripts/
> drwxr-xr-x  2 root root    4096 Sep  7 07:03 src/
> ```


make:

```shell
cd wrk
make
```

make完成之后会有一个wrk的文件，运行此文件即可。

```shell
root@ip-10-100-7-107:~/wrk# ll
total 4372
...
...
-rwxr-xr-x  1 root root 4391168 Sep  7 07:13 wrk*
```

> 如果遇到编译错误:
> ```shell
> fatalerror: openssl/ssl.h: Nosuchfileor directory
> ```
> 需要安装openssl库：
> ```shell
> sudo apt-get install libssl-dev
> # or run
> sudo yum install openssl-devel
>```

## 2. 使用

### 2.1 基本用法

**示例：**

```shell
wrk -t128 -c1000 -d30s --latency http://localhost:3000/
```

这进行了一场拥有128个线程，打开1000个连接，持续30秒的测试, 并会输出详细的用时统计信息。

输出结果：

```shell
Running 30s test @ http://localhost:3000/
  128 threads and 1000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   112.62ms    9.45ms 302.69ms   95.31%
    Req/Sec    64.58     14.91   141.00     84.98%
  Latency Distribution
     50%  112.43ms
     75%  114.48ms
     90%  116.79ms
     99%  119.77ms
  232611 requests in 30.10s, 53.02MB read
  Socket errors: connect 3, read 139, write 9, timeout 0
Requests/sec:   7727.90
Transfer/sec:      1.76MB
```

可用参数解析：

```
-c, --connections: 保持打开状态的 HTTP 连接总数
                   每个线程持有 N = 总连接数 / 总线程数

-d, --duration:    测试持续的时间, e.g. 2s, 2m, 2h

-t, --threads:     使用的总线程数量

-s, --script:      LuaJIT脚本, 参考文件SCRIPTING

-H, --header:      需要向HTTP请求添加的header, 例如 "User-Agent: wrk"

    --latency:     打印详细的延迟统计信息

    --timeout:     如果在这段时间内没有收到响应，则记录超时
```

结果解析:

```shell
Running 30s test @ http://localhost:3000/ # 运行 30秒 测试 @ http://localhost:3000/
  128 threads and 1000 connections # 128线程 1000连接数
    (线程统计)      (平均)     (标准差)   (最大值)     (正负标准差)
  Thread Stats      Avg        Stdev     Max        +/- Stdev
  Latency(延迟)     112.62ms   9.45ms    302.69ms    95.31%
  Req/Sec(请求/秒)  64.58      14.91     141.00      84.98%
  Latency Distribution (延时分布)
     50%  112.43ms  (50%以内的请求在112.43ms之内完成)
     75%  114.48ms  (75%以内的请求在114.48ms之内完成)
     90%  116.79ms  (90%以内的请求在116.79ms之内完成)
     99%  119.77ms  (99%以内的请求在119.77ms之内完成)
  232611 requests in 30.10s, 53.02MB read (在30.10s之内完成了232611个请求, 读取了53.02MB数据)
  Socket errors: connect 3, read 139, write 9, timeout 0 (Socket错误: 连接错误 3，读错误 139，写错误 9，超时 0)
Requests/sec:   7727.90   (每秒请求 7727.90个)
Transfer/sec:      1.76MB (每秒传输数据 1.76MB)
```

### 2.2 Post请求

可以参考项目本身的示例文件，例如`/scripts/post.lua`文件：

```lua
-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.body   = "foo=bar&baz=quux"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
```

简单的在里面定义一下你的请求参数就好，当然也可以使用lua来生成一些随机的内容。

**使用：**
使用`--script=xxx`参数来指定脚本进行压测。

```shell
wrk -t8 -c200 --script=scripts/post.lua -d5m http://xxx.xxx.xxx/xxx/xxx
```
