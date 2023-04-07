package org.oracletracker;

import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.Type;

public class LineNumVisitor extends MethodVisitor {
    public LineNumVisitor(int api) {
        super(api);
    }

    public LineNumVisitor(int api, MethodVisitor methodVisitor) {
        super(api, methodVisitor);
    }

    @Override
    public void visitLineNumber(int line, Label start) {

        super.visitLineNumber(line, start);
    }




}
