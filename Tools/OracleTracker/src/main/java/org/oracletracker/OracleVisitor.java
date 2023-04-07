package org.oracletracker;


import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.Type;

import java.io.File;


public class OracleVisitor extends MethodVisitor {

    private int cur_line;

    private String file;

    public OracleVisitor(int api, MethodVisitor methodWriter, String f) {
        super(api, methodWriter);
        this.file = f;
    }

    public OracleVisitor(int api, String f) {
        super(api);
        this.file = f;
    }

    @Override
    public void visitLineNumber(int line, Label start) {
        cur_line = line;
        super.visitLineNumber(line, start);
    }

    @Override
    public void visitMethodInsn(int opcode, String owner, String name, String descriptor, boolean isInterface) {
        super.visitMethodInsn(opcode, owner, name, descriptor, isInterface);
        if (opcode ==  Opcodes.INVOKESPECIAL && (owner.endsWith("Exception")|| owner.endsWith("Error"))
                && name.equals("<init>")) {

            this.mv.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System", "err", "Ljava/io/PrintStream;");
            this.mv.visitTypeInsn(Opcodes.NEW, Type.getInternalName(StringBuilder.class)); //  "java/lang/StringBuilder"
            this.mv.visitInsn(Opcodes.DUP);
            // Actually, the exception hasn't been thrown yet, but it is one of the candidate exception
            // that the test is going to fail with
            // testthrow/sourcethrow
            //change here.
            this.mv.visitLdcInsn("testthrow " + owner + " " + cur_line + " " + this.file);
            this.mv.visitMethodInsn(Opcodes.INVOKESPECIAL, Type.getInternalName(StringBuilder.class), "<init>", "(Ljava/lang/String;)V", false);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, Type.getInternalName(StringBuilder.class), "toString", "()Ljava/lang/String;", false);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

        }
    }
}
