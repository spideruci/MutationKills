package org.oracletracker;

import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.MethodVisitor;
import java.io.File;

public class OracleTrackingClassVisitor extends ClassVisitor {

    String sourceFile;
    public OracleTrackingClassVisitor(int api, ClassWriter cw, File f) {
        super(api, cw);
        this.sourceFile = null;

    }
    @Override
    public void visitSource(String source, String debug) {
        super.visitSource(source, debug);
        this.sourceFile = source;
    }


    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
        
        if (this.cv != null) {
            MethodVisitor methodWriter = this.cv.visitMethod(access, name, descriptor, signature, exceptions);
            return new OracleVisitor(this.api, methodWriter, this.sourceFile);
        }
        else {
            // mv = new MethodReturnAdapter(Opcodes.ASM4, className, access, name, desc, mv);
            return new OracleVisitor(this.api, this.sourceFile);
        }
    }
    
}
