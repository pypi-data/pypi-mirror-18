# -*- coding: utf-8 -*-
from string import Template
from textwrap import dedent

base_makefile = Template(dedent("""\
    SRC = src
    BUILD = build
    BIN = bin
    EXT = c

    TARGET = $$(BIN)/main

    FLAGS =-std=c99 -Wall -Wextra -pedantic
    INC = -Iinclude
    LIBS =

    CC = gcc

    SRCS = $$(shell find $$(SRC) -name *.$$(EXT))
    OBJS = $$(patsubst $$(SRC)/%, $$(BUILD)/%, $$(SRCS:.$$(EXT)=.o))

    all: $$(TARGET)

    $$(TARGET): $$(OBJS)
    	@mkdir -p $$(BIN)
    	$$(CC) -o $$@ $$(OBJS) $$(LIBS)

    $$(BUILD)/%.o: $$(SRC)/%.$$(EXT)
    	@mkdir -p $$(BUILD)
    	$$(CC) $$(FLAGS) $$(INC) -c -o $$@ $$<

    clean:
    	rm -rf $$(BUILD) $$(BIN)

    test:
    doc:
    """))
