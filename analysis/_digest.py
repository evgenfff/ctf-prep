import json, io, sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('ses_e924a5006ffdiun30gmbdwvorp.json', encoding='utf-8'))
msgs = d['messages']

with io.open('analysis/session_digest.md', 'w', encoding='utf-8') as out:
    for m in msgs:
        t = m.get('type')
        if t in ('user', 'synthetic', 'compaction', 'idle', 'model-switched'):
            out.write('\n\n#### [' + t + '] ' + m['id'] + '\n')
            if t == 'model-switched':
                out.write('switch: %s -> %s\n' % (m.get('previous', {}).get('variant'), m.get('model', {}).get('variant')))
            else:
                out.write((m.get('text') or m.get('summary') or json.dumps(m, ensure_ascii=False)) + '\n')
        elif t == 'assistant':
            txts = [c for c in m.get('content', []) if c['type'] == 'text']
            if txts:
                out.write('\n**A** (' + m['id'][:14] + '): ')
                out.write(' '.join(c.get('text', '') for c in txts) + '\n')

# tool call log
with io.open('analysis/session_tools.md', 'w', encoding='utf-8') as out:
    n = 0
    for m in msgs:
        if m.get('type') != 'assistant':
            continue
        for c in m.get('content', []):
            if c['type'] != 'tool':
                continue
            n += 1
            inp = c.get('state', {}).get('input', {})
            brief = json.dumps(inp, ensure_ascii=False)
            if len(brief) > 300:
                brief = brief[:300] + '...'
            out.write('%4d %-10s %s\n' % (n, c.get('name'), brief))
print('ok', n)
