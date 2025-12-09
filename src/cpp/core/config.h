#ifndef CONFIG_H
#define CONFIG_H

#include "modelos.h"
#include <vector>
#include <string>

const std::vector<std::string> DIAS_SEMANA = {
    "Lunes", "Martes", "Miercoles", "Jueves", "Viernes"
};

const std::vector<std::pair<std::string, std::string>> SLOTS_MATUTINO = {
    {"07:00", "08:00"},
    {"08:00", "09:00"},
    {"09:00", "10:00"},
    {"10:00", "11:00"},
    {"11:00", "12:00"},
    {"12:00", "13:00"},
    {"13:00", "14:00"}
};

const std::vector<std::pair<std::string, std::string>> SLOTS_VESPERTINO = {
    {"14:00", "15:00"},
    {"15:00", "16:00"},
    {"16:00", "17:00"},
    {"17:00", "18:00"},
    {"18:00", "19:00"},
    {"19:00", "20:00"},
    {"20:00", "21:00"}
};

std::vector<Slot> getAllSlots(const std::string& turno);

#endif
