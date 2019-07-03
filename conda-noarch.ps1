$j = C:\Anaconda3\Scripts\conda.exe list -n api --json | convertfrom-json
$j | ?{$_.build_string.startswith('py_')} | %{$_.dist_name}
