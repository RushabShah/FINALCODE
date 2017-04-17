from subprocess import PIPE, Popen
from flask import Flask, request
import random
import os

# p = Popen(["fdisk", "/dev/sdb1"], stdin=PIPE, stdout=PIPE, bufsize=1)
# print p.communicate("m\np\nd\np\nn\n\n\n\n\nt\n8e\np\nw\n")[0]

app=Flask(__name__)

@app.route("/",methods=['GET'])
def FirstPage():
	html='<html><body><form method="POST" action="/CreatePhysical"><label>Enter the number of physical volume to be created : </label><input type="number" name="pvnum"><br><input type="submit" value="Submit"></form></body></html>'
	return html

@app.route("/CreatePhysical",methods=['POST'])
def CreatePhysical():
	pvnum=int(request.form["pvnum"])
	html='<html><body>Enter the paths to the physical volume : <form action="/Physical" method="POST">'
	i=0
	while i<pvnum:
		html=html+'<input type="text" name="pvname'+str(i)+'"><br>'
		i=i+1
	html=html+'<input style="display:none" type="number" value="'+str(pvnum)+'" name="pvnum"><input type="submit" value="Submit"></form></body></html>'
	return html

@app.route("/Physical",methods=['POST'])
def PhysicalLayer():
	pvnum=int(request.form['pvnum'])
	pvnames=[]
	i=0
	while i<pvnum:
		pvnames.append(request.form['pvname'+str(i)])
		i=i+1
	print pvnames
	i=0
	while i<pvnum:
		p = Popen(["fdisk", pvnames[i]], stdin=PIPE, stdout=PIPE, bufsize=1)
		print p.communicate("m\np\nd\np\nn\n\n\n\n\nt\n8e\np\nw\n")[0]
		os.system('partprobe')
		i=i+1

	p = Popen(["pvcreate"]+pvnames, stdin=PIPE, stdout=PIPE, bufsize=1)
	print p.communicate("y\ny\ny\ny\n")[0]
	p = Popen(["pvdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
	lines=p.communicate()[0].split("\n")
	i=0
	pvnames=[]
	while i<len(lines):
		if 'PV Name' in lines[i]:
			if 'not usable' in lines[i+2]:
				pass
			else:
				pvnames.append(lines[i].split('               ')[1])
		i=i+1
	checkboxes=""
	i=0
	while i<len(pvnames):
		checkboxes=checkboxes+'<input type="checkbox" value="'+pvnames[i]+'" name="pvname'+str(i)+'">'+pvnames[i]+'<br>'
		i=i+1

	# print "names : "+str(pvnames)
	html='<html><body><form method="POST" action="/Volume"><label>Enter the name of the logical volume to be created : </label><input name="vgname"><br>Choose the Physical Volume On which to build the Logical Volume<br>'+checkboxes+'<input type="submit" value="Submit"></form></body></html>'
	return html

@app.route("/Volume",methods=['POST'])
def VolumeLayer():
	vgname=request.form['vgname']
	p = Popen(["pvdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
	lines=p.communicate()[0].split("\n")
	i=0
	pvnames=[]
	while i<len(lines):
		if 'PV Name' in lines[i]:
			pvnames.append(lines[i].split('               ')[1])
		i=i+1
	pvnum=len(pvnames)
	pvnames=[]
	i=0
	while i<pvnum:
		if 'pvname'+str(i) in request.form:
			pvnames.append(request.form['pvname'+str(i)])
		i=i+1
	print "vgnames : "+str(pvnames)
	os.system("vgcreate "+vgname+" "+(' '.join(pvnames)))
	os.system('vgdisplay')
	html='<html><body><form method="POST" action="/LPartition"><label> Enter the number of partitions to be created : </label><input type="number" name="lvnum" ><br><input type="submit" value="Submit"></form></body></html>'
	return html

@app.route("/LPartition",methods=['POST'])
def LogicalLayer():
	p = Popen(["vgdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
	lines=p.communicate()[0].split("\n")
	i=0
	vgnames=[]
	while i<len(lines):
		if 'VG Name' in lines[i]:
			vgnames.append(lines[i].split('               ')[1])
		i=i+1

	vgnum=len(vgnames)
	i=0
	htmlVgNames=''
	while i<vgnum:
		htmlVgNames=htmlVgNames+'<option value="'+vgnames[i]+'">'+vgnames[i]+'</option>'
		i=i+1
	htmlFileSys='<option value="msdos">MS-DOS</option><option value="ntfs">NTFS</option><option value="vfat">VFAT</option><option value="fat">FAT</option><option value="ext2">EXT2</option><option value="ext3">EXT3</option><option value="ext4">EXT4</option>'
	lvnum=int(request.form['lvnum'])
	form=''
	i=0
	while i<lvnum:
		form=form+'<label>Name '+str(i+1)+'</label><input name="lvname'+str(i)+'"> &nbsp; <label>Size'+str(i+1)+'</label><input name="lvsize'+str(i)+'"><label>File System '+str(i+1)+'</label><select name="filesys'+str(i)+'">'+htmlFileSys+'</select><label>Logical Volume : </label><select name="vgname'+str(i)+'">'+htmlVgNames+'</select><br>'
		i=i+1
	html='<html><body><form method="POST" action="/createPartition">'+form+'<input type="number" value="'+str(lvnum)+'" name="lvnum" style="display:none;"><br><input type="submit" value="Submit"></form></body></html>'
	return html

@app.route("/createPartition",methods=['POST'])
def createPartition():
	lvnum=int(request.form['lvnum'])
	partNames=[]
	partSizes=[]
	partFileSys=[]
	partVgNames=[]
	i=0
	while i<lvnum:
		partNames.append(request.form['lvname'+str(i)])
		partSizes.append(request.form['lvsize'+str(i)])
		partFileSys.append(request.form['filesys'+str(i)])
		partVgNames.append(request.form['vgname'+str(i)])
		i=i+1

	i=0
	while i<lvnum:
		p = Popen(["lvcreate", "--name" ,partNames[i],"--size", partSizes[i],partVgNames[i]], stdin=PIPE, stdout=PIPE, bufsize=1)
		print p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0]
		#os.system('lvcreate --name '+partNames[i]+' --size '+partSizes[i]+' '+vgname)
		os.system('mkfs.'+partFileSys[i]+' /dev/'+partVgNames[i]+'/'+partNames[i])
		i=i+1

	os.system('lvdisplay')
	return "Logical Partitions Created"

@app.route("/Remove",methods=['GET'])
def Remove():
	html='<html><body><ul><li><a href="/RemovePartition">Remove Logical Partition</a></li><li><a href="/RemoveVolume">Remove Logical Volume</a></li><li><a href="/RemovePhysical">Remove Physical Volume</a></li><li><a href="/RemoveAll">Remove All Logical Partitions, Logical Volumes and Physical Volumes</a></li></ul></body></html>'
	return html

@app.route("/RemovePartition",methods=['GET','POST'])
def RemovePartition():
	if request.method=="POST":
		lvnum=int(request.form['lvnum'])
		i=0
		while i<lvnum:
			if ("lvname"+str(i)) in request.form:
				print request.form["lvname"+str(i)]
				p = Popen(["lvremove", request.form["lvname"+str(i)]], stdin=PIPE, stdout=PIPE, bufsize=1)
				out=p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0].split("\n")
				os.system("lvdisplay")
			i=i+1
		return "Logical Partition Removed."

	else:
		p = Popen(["lvdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
		lines=p.communicate()[0].split("\n")
		i=0
		lvnames=[]
		while i<len(lines):
			if 'LV Path' in lines[i]:
				lvnames.append(lines[i].split('                ')[1])
			i=i+1

		if len(lvnames)==0:
			return "There are no logical partitions to be deleted"
		
		html='<html><body><h1>Select which logical Partition to be Deleted</h1><form action="/RemovePartition" method="POST">'
		i=0
		while i<len(lvnames):
			html=html+'<input type="checkBox" name="lvname'+str(i)+'" value="'+lvnames[i]+'"> '+(lvnames[i].split('/')[-1])+'<br>'
			i=i+1
		html=html+'<input type="number" name="lvnum" style="display:none;" value="'+str(len(lvnames))+'"><input type="submit" value="Submit"></form></body></html>'

		return html

@app.route("/RemoveVolume",methods=['GET','POST'])
def RemoveVolume():
	if request.method=="POST":
		vgnum=int(request.form['vgnum'])
		i=0
		while i<vgnum:
			if ("vgname"+str(i)) in request.form:
				vgname=request.form["vgname"+str(i)]
				p = Popen(["lvdisplay",vgname], stdin=PIPE, stdout=PIPE, bufsize=1)
				lines=p.communicate()[0].split("\n")
				if len(lines)>1:
					return "Cannot delete volume "+vgname+" as there are logical partitions in it"
				print request.form["vgname"+str(i)]
				p = Popen(["vgremove", request.form["vgname"+str(i)]], stdin=PIPE, stdout=PIPE, bufsize=1)
				out=p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0].split("\n")
				os.system("vgdisplay")
			i=i+1
		return "Logical volume removed"

	else:
		p = Popen(["vgdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
		lines=p.communicate()[0].split("\n")
		i=0
		vgnames=[]
		while i<len(lines):
			if 'VG Name' in lines[i]:
				vgnames.append(lines[i].split('               ')[1])
			i=i+1

		if len(vgnames)==0:
			return "There are no logical volumes to be deleted"
		
		html='<html><body><h1>Select which logical Partition to be Deleted</h1><form action="/RemoveVolume" method="POST">'
		i=0
		while i<len(vgnames):
			html=html+'<input type="checkBox" name="vgname'+str(i)+'" value="'+vgnames[i]+'"> '+(vgnames[i].split('/')[-1])+'<br>'
			i=i+1
		html=html+'<input type="number" name="vgnum" style="display:none;" value="'+str(len(vgnames))+'"><input type="submit" value="Submit"></form></body></html>'

		return html

@app.route("/RemovePhysical",methods=['GET','POST'])
def RemovePhysical():
	if request.method=="POST":
		pvnum=int(request.form['pvnum'])
		print pvnum
		i=0
		while i<pvnum:
			if ("pvname"+str(i)) in request.form:
				pvname=request.form["pvname"+str(i)]
				p = Popen(["vgdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
				lines=p.communicate()[0].split("\n")
				if len(lines)>1:
					return "Cannot delete volume "+pvname+" as there are logical volumes in it"
				print request.form["pvname"+str(i)]
				p = Popen(["pvremove", request.form["pvname"+str(i)]], stdin=PIPE, stdout=PIPE, bufsize=1)
				out=p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0].split("\n")
				os.system("pvdisplay")
			i=i+1
		return "Physical volume Removed."

	else:
		p = Popen(["pvdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
		lines=p.communicate()[0].split("\n")
		i=0
		pvnames=[]
		while i<len(lines):
			if 'PV Name' in lines[i]:
				pvnames.append(lines[i].split('               ')[1])
			i=i+1

		if len(pvnames)==0:
			return "There are no physical volumes to be deleted"
		
		html='<html><body><h1>Select which logical Partition to be Deleted</h1><form action="/RemovePhysical" method="POST">'
		i=0
		while i<len(pvnames):
			html=html+'<input type="checkBox" name="pvname'+str(i)+'" value="'+pvnames[i]+'"> '+(pvnames[i].split('/')[-1])+'<br>'
			i=i+1
		html=html+'<input type="number" name="pvnum" style="display:none;" value="'+str(len(pvnames))+'"><input type="submit" value="Submit"></form></body></html>'

		return html

@app.route("/RemoveAll",methods=['GET','POST'])
def RemoveAll():
	if request.method=="POST":
		p = Popen(["lvdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
		lines=p.communicate()[0].split("\n")
		i=0
		lvnames=[]
		while i<len(lines):
			if 'LV Path' in lines[i]:
				lvnames.append(lines[i].split('                ')[1])
			i=i+1
		i=0

		lvnum=len(lvnames)

		while i<lvnum:
			p = Popen(["lvremove", lvnames[i]], stdin=PIPE, stdout=PIPE, bufsize=1)
			out=p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0].split("\n")
			os.system("lvdisplay")
			i=i+1

		p = Popen(["vgdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
		lines=p.communicate()[0].split("\n")
		i=0
		vgnames=[]
		while i<len(lines):
			if 'VG Name' in lines[i]:
				vgnames.append(lines[i].split('               ')[1])
			i=i+1
		vgnum=len(vgnames)
		i=0

		while i<vgnum:
			p = Popen(["vgremove", vgnames[i]], stdin=PIPE, stdout=PIPE, bufsize=1)
			out=p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0].split("\n")
			os.system("vgdisplay")
			i=i+1

		p = Popen(["pvdisplay"], stdin=PIPE, stdout=PIPE, bufsize=1)
		lines=p.communicate()[0].split("\n")
		i=0
		pvnames=[]
		while i<len(lines):
			if 'PV Name' in lines[i]:
				pvnames.append(lines[i].split('               ')[1])
			i=i+1
		pvnum=len(pvnames)
		i=0
		while i<pvnum:
			p = Popen(["pvremove", pvnames[i]], stdin=PIPE, stdout=PIPE, bufsize=1)
			out=p.communicate("y\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\ny\n")[0].split("\n")
			os.system("pvdisplay")
			i=i+1

		return "Everything Gone From Pendrive"

	else:
		html='<html><body><h1>Are you sure you want to delete Everything</h1><form method="POST" action="/RemoveAll"><input type="submit" value="Yes"></form></body></html>'
		return html

if __name__=='__main__':
	app.run()