## Copyright (C) 2016 Darlan Cavalcante Moreira
## 
## This program is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

## -*- texinfo -*- 
## @deftypefn {Function File} {@var{retval} =} lms (@var{input1}, @var{input2})
##
## @seealso{}
## @end deftypefn

## Author: Darlan Cavalcante Moreira <darlan@darlan-desktop-gtel>
## Created: 2016-11-16

function w = LMS(w0,u,d,s)
%w = LMS(w0,u,d,s)
%LMS alorithm
%INPUT
% w0: [M,1] : Init weight vector, M = Number of taps
% u : [N,1] : Input data vector
% d : [N,1] : Desired output data vector
% s : [1,1] : step-size parameter
%OUTPUT
% w : [M,1] : final tap weight vector
if (nargin<4) error('Too few parameters'); end;
N = length(u);
M = length(w0);
w = w0;
x = zeros(M,1);
for k=1:N
x = [u(k);x(1:M-1)];
ek = d(k) - w'*x;
dw = s * conj(ek) * x;
w = w + dw;
end;