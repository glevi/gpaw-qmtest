import sys
import string
import prog1
usage='Usage: %s qmscr param' % sys.argv[0]

try:
  qmscr=sys.argv[1]; param=sys.argv[2]
except:
  print usage; sys.exit(1)

scr=open(qmscr, 'r') 
lines=scr.readlines(); scr.close()

pr=open(param, 'r')
p=pr.readlines(); pr.close()  

for n,line in enumerate(p):
  if 'Progression' in line:
    sp=[float(x) for x in p[n+2].split()] 
    if 'geom' in line:
      h=prog1.geomprog(sp[0], sp[1], sp[2])
    elif 'art' in line:
      h=prog1.artprog(sp[0], sp[1], sp[2])
    p[:n-1]=[basis.strip() for basis in p[:n-1]]
    bnames=p[:n-1]
    bnames=[basis.replace('(', '') for basis in bnames]
    bnames=[basis.replace(')', '') for basis in bnames]
    b={}
    for name, basis in zip(bnames, p[:n-1]):
      b[name]=basis


for name in b: 
  for k in range(len(h)):
    nlines=lines    
    scrpy=open(qmscr+'_%s_%.3f.py' %  (name, h[k]), 'w')   
    nlines=[string.replace('basis=', "basis='%s'" % (b[name])) for string in nlines]
    nlines=[string.replace('h=', 'h=%.3f' % (h[k])) for string in nlines]  
    nlines=[string.replace('txt=()', "txt=('"+qmscr+"_%s_%.3f.out')" % (name, h[k])) for string in nlines]
    nlines=[string.replace('open()', "open('"+qmscr+"_%s_%.3f.txt', 'w')" % (name, h[k])) for string in nlines]
    nlines=[string.replace('trajectory=', "trajectory='"+qmscr+"_%s_%.3f.traj'" % (name, h[k])) for string in nlines]
    nlines=[string.replace('logfile=', "logfile='"+qmscr+"_%s_%.3f.log'" % (name, h[k])) for string in nlines]
    nlines=[string.replace('calc.write()', "calc.write('"+qmscr+"_%s_%.3f.gpw', mode='all')" % (name, h[k])) for string in nlines]
    for i,line in enumerate(lines):
      if "print('Basis set        Grid spacing', file=fd)" in line:
        nlines.insert(i+1, "print('%s             %.3f', file=fd)\n" % (name, h[k]))
    for q,line in enumerate(lines): 
      if "print('Basis set        Grid spacing        dPt-Pt        dP-Pt', file=fd)" in line:
        nlines.insert(q+2, "print('%s                %.3f              %%5.4f         %%5.4f' %% (dn, dn_1), file=fd)\n" % (name, h[k]))
    scrpy.writelines(nlines)
    scrpy.close()

