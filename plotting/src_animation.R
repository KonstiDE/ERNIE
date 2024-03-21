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
        ggtitle(date)

    ggsave(paste0("news_", sub(" ", "_", as.character(date)), ".png"), p)
}


# Bar plot for distribution of it #
tpkg <- pkg
tpkg$date <- lubridate::round_date(tpkg$date, unit = "hour")

dateagg_us <- data.frame(
    date = unique(tpkg$date),
    count = aggregate(tpkg, by = "date", count = T)$agg_n
)
dateagg_us <- rbind(data.frame(
    date = make_datetime(2024, 1, 1, 7),
    count = 0
), dateagg_us)

ggplot() +
    geom_line(data = dateagg_us, mapping = aes(x = date, y = count), stat = "identity")


# Try to add time zones #
time_zones <- read.csv("time_zone.csv")
country_names <- read.csv("country.csv")

tpc <- aggregate(gmt_offset ~ country_code, time_zones, median)
tpc <- left_join(country_names, tpc, by = "country_code", unmatched = "drop")

tpc$country_code[tpc$country_name == "Namibia"] <- "NA"
tpc$gmt_offset[tpc$country_name == "Namibia"] <- "7200"
tpc$country_code[tpc$country_code == "GB"] <- "UK"
tpc <- rbind(tpc, data.frame(
    country_code = "XK",
    country_name = "Kosovo",
    gmt_offset = "3600"
))
tpc$TLD <- paste0(".", tolower(tpc$country_code))

tpc <- left_join(pkg, tpc, by = join_by(TLD == TLD), relationship = "many-to-many")

tpc$gmt_offset <- as.numeric(tpc$gmt_offset)
tpc$date <- tpc$date - seconds(tpc$gmt_offset)
tpc$date <- tpc$date + seconds(9 * 60 * 60)

tpc <- tpc[order(tpc$date),]

a = data.frame(tpc)

end_date <- tpc[length(tpc$date)]$date
start_date <- tpc[1]$date

dates <- seq(from = start_date, to = end_date, by='1 hours')

suppressWarnings({
    for(date in dates){
        m <- tpc[tpc$date <= date]

        agg <- data.frame(
            NAME_0 = unique(m$NAME_0),
            count = aggregate(m, by = "NAME_0", count = T)$agg_n
        )

        countries_c <- merge(countries, agg, all.x=TRUE, by.x = "NAME_0", by.y = "NAME_0")
        countries_csf <- st_as_sf(countries_c)

        p <- ggplot() +
            geom_spatvector(data = countries_c, mapping = aes(fill = count)) +
            scale_fill_distiller(palette = "YlGnBu", name="Amount of articles", trans = "log", limits = c(1, 1000)) +
            ggtitle(paste(
              paste(day(date), ". Januar", year(date)),
              paste(hour(date), "00", sep = ":")
            ))

        ggsave(paste0("news_", sub(" ", "_", as.character(date)), ".png"), p)
    }
})






