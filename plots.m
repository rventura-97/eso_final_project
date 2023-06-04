%% Read data
cd REPORTS
health_metrics = readtable("health_metrics_mean.csv");
econ_metrics = readtable("econ_metrics_mean.csv");
cd ..

%% Format data
health_metrics_local = health_metrics(health_metrics.TypeOfMonitoring=="LOCAL",:);
health_metrics_local.AppointmentsInterval = str2double(health_metrics_local.AppointmentsInterval);
health_metrics_local = sortrows(health_metrics_local, "AppointmentsInterval");

health_metrics_remote = health_metrics(health_metrics.TypeOfMonitoring=="REMOTE",:);
health_metrics_remote.RPMRecall = str2double(health_metrics_remote.RPMRecall);
health_metrics_remote = sortrows(health_metrics_remote, "RPMRecall");

econ_metrics_local = econ_metrics(econ_metrics.TypeOfMonitoring=="LOCAL",:);
econ_metrics_local.AppointmentsInterval = str2double(econ_metrics_local.AppointmentsInterval);
econ_metrics_local = sortrows(econ_metrics_local, "AppointmentsInterval");

econ_metrics_remote = econ_metrics(econ_metrics.TypeOfMonitoring=="REMOTE",:);
econ_metrics_remote.RPMRecall = str2double(econ_metrics_remote.RPMRecall);
econ_metrics_remote = sortrows(econ_metrics_remote, "AppointmentsInterval");

%% Plot ICU death rates
fig = figure();

hold on;
plot(health_metrics_local.ICUDeathRate,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(health_metrics_remote.ICUDeathRate,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("ICU Death Rate");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%% Plot critical death rates
fig = figure();

hold on;
plot(health_metrics_local.CriticalDeathRate,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(health_metrics_remote.CriticalDeathRate,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("Critical Death Rate");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%% Plot early diagnoses rate
fig = figure();

hold on;
plot(health_metrics_local.EarlyDiagnosesRate,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(health_metrics_remote.EarlyDiagnosesRate,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("Early Diagnoses Rate");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%% Plot critical state reversals rate
fig = figure();

hold on;
plot(health_metrics_local.CriticalityReversalRate,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(health_metrics_remote.CriticalityReversalRate,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("Critical Reversals Rate");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%% Plot mean icu occupancy
fig = figure();

hold on;
plot(health_metrics_local.MeanICUOccupancy,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(health_metrics_remote.MeanICUOccupancy,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("Mean ICU Occupancy (Patients)");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%% Plot mean icu stay
fig = figure();

hold on;
plot(health_metrics_local.MeanICUStay,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(health_metrics_remote.MeanICUStay,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("Mean ICU Stay (Days)");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%% Plot required number of doctors for monitoring patients
fig = figure();
hold on;
plot(econ_metrics_local.NumberOfDoctors,...
     "LineStyle","--","Color","r",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","r");
plot(econ_metrics_remote.NumberOfDoctors,...
     "LineStyle","--","Color","b",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","b");
hold off;
grid on;
legend("Local Monitoring", "Remote Monitoring", Location="east");
axis('padded');
ax1 = gca;
ax1_pos = ax1.Position;
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','left', ...
    'Color','none') ;
ax2.XLim = ax1.XLim ;
ax2.YLim = ax1.YLim ;
ax1.XColor = "r";
ax2.XColor = "b";
xlabel(ax1, 'Appointments Interval (days)');
xlabel(ax2, 'Recall');
ylabel("Required Cardiologists for Monitoring");
xticklabels(ax1,health_metrics_local.AppointmentsInterval);
xticklabels(ax2,health_metrics_remote.RPMRecall);
fontsize(fig, 24, "points");

%%
fig = figure();
plot(health_metrics_local.AppointmentsInterval,econ_metrics_local.TotalCost,...
     "LineStyle","--","Color","k",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","k");
grid on;
axis('padded');
fontsize(fig, 24, "points");
ylabel("Total Cost (M€)");
xlabel('ICU Death Rate');

%% Plot total cost as function of death rate (local monitoring)
fig = figure();
plot(health_metrics_local.ICUDeathRate,econ_metrics_local.TotalCost,...
     "LineStyle","--","Color","k",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","k");
grid on;
axis('padded');
fontsize(fig, 24, "points");
ylabel("Total Cost (M€)");
xlabel('ICU Death Rate');

%% Plot total cost as function of death rate (remote monitoring)
fig = figure();
plot(health_metrics_remote.ICUDeathRate,econ_metrics_remote.TotalCost,...
     "LineStyle","--","Color","k",'MarkerSize',15,"Marker","o","LineWidth",5,"MarkerFaceColor","k");
grid on;
axis('padded');
fontsize(fig, 24, "points");
ylabel("Total Cost (M€)");
xlabel('ICU Death Rate');

%% Plot cumulative cost (local monitoring)
fig = figure();
hold on;
plot(table2array(econ_metrics_local(1,9:end)),...
     "LineStyle","-","Color","k","LineWidth",5);
plot(table2array(econ_metrics_remote(1,9:end)),...
     "LineStyle","-","Color","k","LineWidth",5);

%% Plot cumulative cost (remote monitoring)
fig = figure();
hold on;
plot(table2array(econ_metrics_remote(1,9:end)),...
     "LineStyle","-","Color","k","LineWidth",5);


%% Plot total cost distribution (local monitoring)
fig = figure();
bar(table2array(econ_metrics_local(:,6:7)),'stacked');
xticklabels(econ_metrics_local.AppointmentsInterval);
legend("ICU","Doctors");

%% Plot total cost distribution (remote monitoring)
fig = figure();
bar(table2array(econ_metrics_remote(:,6:8)),'stacked');
xticklabels(econ_metrics_remote.RPMRecall);
legend("ICU","Doctors","RPM");