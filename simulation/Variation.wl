(* Define the parameters and differential equations *)
sigma = 10; beta = 8/3; rho = 28;

lorenzSystem = {
  x'[t] == sigma * (y[t] - x[t]),
  y'[t] == x[t] * (rho - z[t]) - y[t],
  z'[t] == x[t] * y[t] - beta * z[t],
  x[0] == 1, y[0] == 1, z[0] == 1
};

(* Numerically solve the ODE system for t from 0 to 100 *)
sol = NDSolve[lorenzSystem, {x, y, z}, {t, 0, 100}];

(* Render the 3D parametric trajectory *)
ParametricPlot3D[
  Evaluate[{x[t], y[t], z[t]} /. sol], 
  {t, 0, 100}, 
  PlotRange -> All, 
  ColorFunction -> "Rainbow", 
  Boxed -> False, 
  Axes -> False,
  Plotப்பிட -> 0.02
]
(* System Parameters for 5D Hyperchaos *)
a = 49; b = 8; c = 180; p = 6;

system5D = {
  x1'[t] == a * (x2[t] - x1[t]) + x2[t] * x3[t] + x3[t] + x4[t] + x5[t],
  x2'[t] == c * x2[t] - x1[t] * x3[t] + x4[t] + x5[t],
  x3'[t] == x1[t] * x2[t] - b * x3[t],
  x4'[t] == -p * (x1[t] + x2[t]),
  x5'[t] == -x1[t],
  x1[0] == 0.2, x2[0] == 0.1, x3[0] == 0.2, x4[0] == 0.1, x5[0] == 0.2
};

(* Numerically solve the 5D ODE system *)
sol = NDSolve[system5D, {x1, x2, x3, x4, x5}, {t, 0, 40}];

(* Visualize 3D spatial projection with 4th dimension driving the color *)
ParametricPlot3D[
  Evaluate[{x1[t], x2[t], x3[t]} /. sol], 
  {t, 0, 40}, 
  ColorFunction -> Function[{x, y, z, t}, Hue[(x4[t] /. sol[[1]]) / 50]], 
  ColorFunctionScaling -> False,
  PlotRange -> All, 
  Boxed -> False, 
  Axes -> False,
  PlotStyle -> Directive[Thickness[0.002]]
]
(* Parameters and State Variables *)
a = 49; b = 8; c = 180; p = 6;
vars = {x1[t], x2[t], x3[t], x4[t], x5[t]};

(* Right-hand side of the 5D system *)
f = {
  a * (x2[t] - x1[t]) + x2[t] * x3[t] + x3[t] + x4[t] + x5[t],
  c * x2[t] - x1[t] * x3[t] + x4[t] + x5[t],
  x1[t] * x2[t] - b * x3[t],
  -p * (x1[t] + x2[t]),
  -x1[t]
};

(* Compute the Jacobian matrix J_ij = D[f_i, x_j] *)
jacobian = Outer[D, f, vars];

(* Base system coupled with initial conditions *)
baseSys = Thread[D[vars, t] == f] /. {
  x1[0] -> 0.2, x2[0] -> 0.1, x3[0] -> 0.2, x4[0] -> 0.1, x5[0] -> 0.2
};

(* Numerical integration to capture the trajectory for linearization *)
sol = NDSolveValue[baseSys, vars, {t, 0, 100}];
