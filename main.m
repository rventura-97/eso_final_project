%%
x = 0:0.01:100;

L1 = 0.7./(1+exp(-0.1*(x-80)));
L2 = 0.7./(1+exp(-0.01*(x-80)));
figure;
hold on;
plot(x,L1);
plot(x,L2);
grid on;

%%
t = 0:1:28;
f = (1-28*(0.0005467524155392312)) + t*0.0005467524155392312;
figure;
plot(t,f);
hold off;
surv_prob = prod(f);


%%
t = 0:1:28;
f = 0.02*t;
figure;
plot(t,f);
surv_prob = prod(f);

%%
syms p;
f = 1;
for t = 1:28
    f = f*(1-t*p);
end

