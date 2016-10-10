# -*- mode: makefile -*-
#
# Makefile containing platform dependencies different projects.
MAKEFLAGS = --no-print-directory -r -s -j2


CXXFLAGS += -Wall -Wno-overloaded-virtual -Wno-unused $(shell root-config --cflags)

LIBS += $(shell root-config --libs) -L${ROOTLIBS} -lTreePlayer -lutil  -lRooFit -lRooFitCore  \
	-lRooStats -lFoam -lMinuit -lHistFactory  -lXMLParser -lXMLIO -lCore 

#./bin/qmuToys
TARGETS = ./get_limits

all: 	${TARGETS}

OBJS=runAsymptoticsCLs.o

get_limits: get_limits.C $(OBJS)
	@echo "Compiling " $@
	@echo $(CXX) $(CXXFLAGS) $< $(OBJS) $(LIBS) -o $@
	@$(CXX) $(CXXFLAGS) $< $(OBJS) $(LIBS) -o $@

%.o : %.C
	@echo "Compiling $<"runAsymptoticsCLs
	@$(CXX) $(CXXFLAGS) -O2 -c $< -o $@ $(INCLUDES)

clean:
		@echo "Cleaning $<..."
		@rm -f *~ *.o */*~ *_Dict.* *.a get_limits
		@echo "Done"
	
