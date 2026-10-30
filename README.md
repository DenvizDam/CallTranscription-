

find /mnt /home -type d -name "data_PRD" 2>/dev/null

df -hT | grep -Ei 'cifs|nfs|smb'
