	dimension a(1000,1000), b(1000,1000)
	open(1,file='borra1')
	open(2,file='borra2')
	print*, 'hola'
	x10a=1
c	x10b=0.4
	nx=1000
	ny=388
	xl=8
	yl=4
	xs=2*xl/(nx-1)
	ys=2*yl/(ny-1)
	do i=1,ny
	   do j=1,ny
	      read (1,*) a(i,j)
	   end do
	end do
	do x1=-xl,xl,xs
	   do x2=-xl,xl,xs
	      xm2a=x1*x1+(x2-x10a)*(x2-x10a)+0.0001
c	      xm2b=x1*x1+(x2-x10b)*(x2-x10b)+0.0001
	      y1=x1-x1/xm2a
              y2=x2-(x2-x10a)/xm2a
c	      y1=x1
c	      y2=x2
	      i1=(y1+yl)/ys+1
	      i2=(y2+yl)/ys+1
	      j1=1+(nx-1)*(x1+xl)/(2*xl)
	      j2=1+(nx-1)*(x2+xl)/(2*xl)
c	      print*, i1,i2,j1,j2
	      if ((i1.ge.1).and.(i1.le.ny).and.(i2.ge.1).and.(i2.le.ny)) then
	         b(j1,j2)=a(i1,i2)
              else
		 b(j1,j2)=3000
	      end if
      	    end do
	 end do
	do i=1,nx
	   do j=1,nx
	      write (2,*) b(i,j)
	   end do
	end do
	end
	 
		
