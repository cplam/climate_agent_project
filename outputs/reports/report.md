# Global Mean Temperature Change (2016–2025)

Data and methods
- Source: Copernicus Climate Data Store (CDS), ERA5 monthly-averaged reanalysis (single levels).
- Dataset: reanalysis-era5-single-levels-monthly-means; variable: 2m_temperature; years: 2016–2025; months: Jan–Dec; time: 00:00; format: NetCDF.
- Processing: Monthly data aggregated to annual means (saved to outputs/data/simulated_temperature.csv); linear regression applied to estimate the trend. Visualization saved to outputs/figures/temperature_trend.png.

Main findings
- Estimated linear trend: 0.3473 °C per year (~3.47 °C per decade) in global mean 2m temperature over 2016–2025.
- The time series indicates a pronounced warming signal across the decade in ERA5.

Caveats and limitations
- Short window (10 years) can be strongly influenced by interannual variability (e.g., ENSO) and may overstate/understate longer-term rates.
- ERA5 is a reanalysis (model–data blend); results may differ from purely observational products (e.g., NASA GISTEMP, NOAA, Berkeley Earth).
- Uncertainty and formal significance testing are not reported here; non-parametric checks were planned but are not included in these results.

Conclusion
- ERA5 data for 2016–2025 show a strong upward trend in global mean near-surface temperature.
- For robust assessment and decision-making, validate against multiple datasets and extend analysis to longer periods with uncertainty and significance metrics.