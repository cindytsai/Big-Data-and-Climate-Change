% file dependent, 
Z = TEMPAVGFFT;
Z = log10(Z);
Z_unit = 'Magnitude';
colorbar_string = '';
title_name = 'Average Temperature (Discrete Fourier Transform -> LOG(mag))';
sample_rate = floor(365/2);
start_year = 1933;
end_year = 2018;


%===========================================%
% X is imported
YEAR = [start_year:end_year];

% Plot
surf(X, YEAR, Z)
colormap('jet')
cbar = colorbar;
cbar.Label.String = colorbar_string;
cbar.Label.FontSize = 16;
title(title_name, 'Color', 'b', 'FontSize', 18)
xlim([min(X) max(X)])
xlabel('Frequency (Hz)', 'FontSize', 16)
yticks([start_year, (fix(start_year/10)+1)*10:10:fix(end_year/10)*10,end_year])
ylim([start_year, end_year])
ylabel('YEAR', 'FontSize', 16)
zlabel(Z_unit, 'FontSize', 16)
