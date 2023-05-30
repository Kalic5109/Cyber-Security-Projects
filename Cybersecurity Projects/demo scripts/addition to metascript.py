# cat interact_with_filter.py https://stackoverflow.com/questions/43371249/using-expect-and-interact-simultaneously-in-pexpect
import pexpect, re

def output_filter(s):
    global proc, bash_prompt, filter_buf, filter_buf_size, let_me_out

    filter_buf += s
    filter_buf = filter_buf[-filter_buf_size:]

    if "LET ME OUT" in filter_buf:
        let_me_out = True

    if bash_prompt.search(filter_buf):
        if let_me_out:
            proc.sendline('exit')
            proc.expect(pexpect.EOF)
            proc.wait()
        else:
            proc.sendline('python')

    return s

filter_buf = ''
filter_buf_size = 256
let_me_out = False
bash_prompt = re.compile('bash-[.0-9]+[$#] $')

proc = pexpect.spawn('bash --noprofile --norc')
proc.interact(output_filter=output_filter)