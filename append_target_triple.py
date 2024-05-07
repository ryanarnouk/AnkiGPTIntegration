import subprocess
import sys
import os
import asyncio
import re

extension = ''
if sys.platform == 'win32':
    extension = '.exe'

async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()

async def main():
    rust_info, _ = await run_command('rustc -vV')
    target_triple = re.search(r'host: (\S+)', rust_info).group(1)
    if not target_triple:
        print('Failed to determine platform target triple')
        return
    os.rename(
        f'dist/api{extension}',
        f'dist/api-{target_triple}{extension}'
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        raise e