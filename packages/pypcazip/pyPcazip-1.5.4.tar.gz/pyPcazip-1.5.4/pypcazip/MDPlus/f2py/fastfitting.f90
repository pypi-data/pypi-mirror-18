! Fast fitting function to be wrapped with f2py...
subroutine fitted_traj(traj, ref, w, out, n, nframes)
! fits every snapshot in rawfile to structure ref and returns the
! the result in out.
! In the python function w is an optional argument, but due to a bug
! in f2py it will, if absent, still be passed with a value of zero, so
! the code checks for this.
!
  real*4, intent(in)  :: traj(nframes,n,3)
  real*4, intent(in)        :: ref(n,3)
  real*4, intent(in), optional :: w(n,3)
  real*4, intent(out)       :: out(nframes,n,3)
  integer, intent(in)       :: n, nframes

  integer                   :: i, j, k, m
  real*4                    :: wloc(n), r(3,3), v(3), rms, in(3,n)
  logical                   :: dofit

  dofit=.true.
  
  if (maxval(w) == 0) then
      wloc = 1.0
  else
      wloc = w(:,1)
  endif

  out = 0.0
  do m = 1, nframes
      in = transpose(traj(m,:,:))
      call matfitw(n,transpose(ref),in,r,v,rms,dofit,wloc)

      do i=1,n
        do j=1,3
          out(m,i,j) = out(m,i,j) + v(j)
          do k=1,3
            out(m,i,j) = out(m,i,j) + r(j,k)*in(k,i)
          end do
        end do
      end do
  end do

end subroutine fitted_traj

subroutine fitted(in, ref, w, out, n)
! Fits in to structure ref and returns the
! the result in out.
!
  real*4, intent(in)        :: in(n,3)
  real*4, intent(in)        :: ref(n,3)
  real*4, intent(in), optional :: w(n,3)
  real*4, intent(out)       :: out(n,3)
  integer, intent(in)       :: n

  integer                   :: i, j, k, m
  real*4                    :: wloc(n), r(3,3), v(3), rms
  logical                   :: dofit

  dofit=.true.
  
  if (maxval(w) == 0) then
      wloc = 1.0
  else
      wloc = w(:,1)
  endif

  out = 0.0
  call matfitw(n,transpose(ref),transpose(in),r,v,rms,dofit,wloc)

  do i=1,n
    do j=1,3
      out(i,j) = out(i,j) + v(j)
      do k=1,3
        out(i,j) = out(i,j) + r(j,k)*in(i,k)
      end do
    end do
  end do

end subroutine fitted

subroutine rv(in, ref, w, r, v, n)
! Fits in to structure ref and returns the
! the rotation matrix and shift vector.
!
  real*4, intent(in)        :: in(n,3)
  real*4, intent(in)        :: ref(n,3)
  real*4, intent(in), optional :: w(n,3)
  real*4, intent(out)       :: r(3,3)
  real*4, intent(out)       :: v(3)
  integer, intent(in)       :: n

  integer                   :: i, j, k, m
  real*4                    :: wloc(n), rms
  logical                   :: dofit

  dofit=.true.
  
  if (maxval(w) == 0) then
      wloc = 1.0
  else
      wloc = w(:,1)
  endif

  out = 0.0
  call matfitw(n,transpose(ref),transpose(in),r,v,rms,dofit,wloc)

end subroutine rv

subroutine rmsd_traj(traj, ref, w, out, n, nframes)
! fits every snapshot in rawfile to structure ref and returns the
! the rmsd in out.
!
  real*4, intent(in)  :: traj(nframes,n,3)
  real*4, intent(in)        :: ref(n,3)
  real*4, intent(in), optional :: w(n,3)
  real*4, intent(out)       :: out(nframes)
  integer, intent(in)       :: n, nframes

  integer                   :: i, j, k, ios, m
  real*4                    :: wloc(n), r(3,3), v(3), rms, in(3,n)
  logical                   :: dofit

  dofit=.false.

  if (maxval(w) == 0) then
      wloc = 1.0
  else
      wloc = w(:,1)
  endif

  out = 0.0
  do m = 1, nframes
      in = transpose(traj(m,:,:))
      call matfitw(n,transpose(ref),in,r,v,rms,dofit,wloc)

      out(m) = rms
  end do

end subroutine rmsd_traj

subroutine rmsd(in, ref, w, out, n)
! Calculates the (optionally mass-weighted) rmsd between in and ref, returns 
! the result in out.
!
  real*4, intent(in)        :: in(n,3)
  real*4, intent(in)        :: ref(n,3)
  real*4, intent(in), optional :: w(n,3)
  real*4, intent(out)       :: out
  integer, intent(in)       :: n

  real*4                    :: wloc(n), r(3,3), v(3), rms
  logical                   :: dofit

  dofit=.false.

  if (maxval(w) == 0) then
      wloc = 1.0
  else
      wloc = w(:,1)
  endif

  call matfitw(n,transpose(ref),transpose(in),r,v,rms,dofit,wloc)

  out = rms

end subroutine rmsd

subroutine fitted_avg(traj, ref, w, out, n, nframes)
! fits every snapshot in rawfile to structure ref and returns the
! the average result in out.
!
  real*4, intent(in)        :: traj(nframes,n,3)
  real*4, intent(in)        :: ref(n,3)
  real*4, intent(in), optional :: w(n,3)
  real*4, intent(out)       :: out(n,3)
  integer, intent(in)       :: n, nframes

  integer                   :: i, j, k, m
  real*4                    :: wloc(n), r(3,3), v(3), rms, in(3,n)
  logical                   :: dofit

  dofit=.true.

  if (maxval(w) == 0) then
      wloc=1.0
  else
      wloc = w(:,1)
  endif

  out = 0.0
  do m = 1, nframes
      in = transpose(traj(m,:,:))
      call matfitw(n,transpose(ref),in,r,v,rms,dofit,wloc)

      do i=1,n
        do j=1,3
          out(i,j) = out(i,j) + v(j)
          do k=1,3
            out(i,j) = out(i,j) + r(j,k)*in(k,i)
          end do
        end do
      end do
  end do

  out = out/nframes

end subroutine fitted_avg

subroutine pib(coords, box, out, nframes, natoms)
!
! Fast version of "pack into box" in utils.py
!
! Wraps coordinates into the primary unit cell
!

  real*4, intent(in)  :: coords(nframes,natoms,3)
  real*4, intent(out)  :: out(nframes,natoms,3)
  real*4, intent(in)        :: box(nframes,3,3)
  integer, intent(in)       :: nframes, natoms

  integer                   :: i, j, k, m
  real*4                    :: boxinv(3), s

  do j = 1, nframes
      boxinv(1) = 1.0/box(j, 1,1)
      boxinv(2) = 1.0/box(j, 2,2)
      boxinv(3) = 1.0/box(j, 3,3)

      do i = 1, natoms
          s = floor(coords(j, i,3) * boxinv(3))
          out(j, i,3) = coords(j, i,3) - s * box(j, 3,3)
          out(j, i,2) = coords(j, i,2) - s * box(j, 3,2)
          out(j, i,1) = coords(j, i,1) - s * box(j, 3,1)

          s = floor(coords(j, i,2) * boxinv(2))
          out(j, i,2) = out(j, i,2) - s * box(j, 2,2)
          out(j, i,1) = out(j, i,1) - s * box(j, 2,1)

          s = floor(coords(j, i,1) * boxinv(1))
          out(j, i,1) = out(j, i,1) - s * box(j, 1,1)
      end do

  end do
end subroutine pib
