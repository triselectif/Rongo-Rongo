################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/appsServer.cpp \
../src/rrInit.cpp 

OBJS += \
./src/appsServer.o \
./src/rrInit.o 

CPP_DEPS += \
./src/appsServer.d \
./src/rrInit.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I/usr/include/dbus-c++-1/ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

src/rrinit_adaptor.h: ../src/rrinit-introspect.xml
	@echo 'Building file: $<'
	@echo 'Invoking: Resource Custom Build Step'
	dbusxx-xml2cpp rrinit-introspect.xml --adaptor=rrinit_adaptor.h
	@echo 'Finished building: $<'
	@echo ' '


