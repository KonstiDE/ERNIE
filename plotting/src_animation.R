setwd("C:/Users/Konstantin/Desktop/noto_plots_test")

library(ggplot2)
library(terra)
library(lubridate)
library(dplyr)
library(sf)
library(viridisLite)
library(classInt)
library(tidyterra)
library(RColorBrewer)

# Animation
pkg <- vect("gadm_cctld_centroid_joined_4326.gpkg")

countries <- vect("gadm_cctld_shortened.gpkg")
countries_no_data <- vect("no_data.gpkg")

pkg$date <- lubridate::as_datetime(pkg$date)
pkg <- pkg[order(pkg$date),]

end_date <- pkg[length(pkg$date)]$date
start_date <- pkg[1]$date

dates <- seq(from = start_date, to = end_date, by='15 mins')

for(date in dates){
    m <- pkg[pkg$date <= date]

    agg <- data.frame(
        NAME_0 = unique(m$NAME_0),
        count = aggregate(m, by = "NAME_0", count = T)$agg_n
    )

    countries_c <- merge(countries, agg, all.x=TRUE, by.x = "NAME_0", by.y = "NAME_0")
    countries_csf <- st_as_sf(countries_c)

    p <- ggplot() +
        geom_spatvector(data = countries_c, mapping = aes(fill = count)) +
        scale_fill_gradientn(colors = turbo(50), limits = c(0, 1466)) +
        ggtitle(m[x,]$date)

    ggsave(paste0("news_", sub(" ", "_", as.character(date)), ".png"), p)
}


# Bar plot for distribution of it #

