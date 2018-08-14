# Good and recommended practices

Once *you have* [KernelUpgrader](https://github.com/Javinator9889/KernelUpgrader) installed, maybe you are wondering 
what are good practices in order to take advantage of this tool.

### How to better use KernelUpgrader

First of all, if you **have installed** a new kernel from source at least once, you should notice that the compilation 
time takes *so long* and do not let you to use your PC normally. So here I will recommend you some tips so you can use 
this tool and make everything easier.

#### Running in background easily

We are going to use a tool called `screen`. This application will let us run *everything we want* in a **background 
process** or in a **foreground one**. For this purpose:

```bash
sudo apt-get install screen
# Create a new screen session with a custom name
screen -dmS linux-kernel
# Go to the created screen
screen -r linux-kernel
```
Now, at the *created screen session*:
```bash
sudo kernel_upgrader
# This will start the tool - use kernel_upgrader -h to see available options
```
So, as far as we got, we have done almost the same like the "normal process". So, what is the point? 

The possibility to **attach** and **detach** whenever we want. For resuming screen, we just write `screen -r`. Inside 
the screen, for going back to our terminal and *detach* it, we press the following buttons combination:

<kbd>CTRL</kbd> <kbd>A</kbd> <kbd>D</kbd> (Ctrl + a + d) - this will make the screen session keep running in background.

#### Viewing logs/process in real time

As you may have appreciated, the UI of KernelUpgrader is **very minimalist**: it is only displaying a little information
 of what *it is doing*. As said in the **program full usage** (`kernel_upgrader -u`), two different logs are being 
 stored while executing:
 + `kernel_upgrader.log`, which saves basic logging about the progress of the execution.
 + `kernel_upgrader.compiler.log`, which is constantly saving the compilation output and progress.

So, in order to watch while executing the *real progress and logs*, we can easily run a simple built-in command that 
will tell us all the information we need:
```bash
# For KernelUpgrader progress
tail -f /var/log/kernel_upgrader.log
```
```bash
# For kernel compilation process
tail -f /var/log/kernel_upgrader.compiler.log
```
Those commands will display all the new lines that are being written to the file chosen.

For stop displaying the output, just run: <kbd>CTRL</kbd> <kbd>C</kbd> (Ctrl + C) - will interrupt command execution.
