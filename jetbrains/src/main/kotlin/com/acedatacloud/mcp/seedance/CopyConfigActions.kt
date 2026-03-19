package com.acedatacloud.mcp.seedance

import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import java.awt.Toolkit
import java.awt.datatransfer.StringSelection

class CopyStdioConfigAction : AnAction("Copy STDIO Config", "Copy STDIO MCP configuration for AI Assistant", null) {
    override fun actionPerformed(e: AnActionEvent) {
        val config = McpSettings.getInstance().getStdioConfig()
        val clipboard = Toolkit.getDefaultToolkit().systemClipboard
        clipboard.setContents(StringSelection(config), null)

        NotificationGroupManager.getInstance()
            .getNotificationGroup("Seedance MCP")
            .createNotification(
                "STDIO config copied! Paste into Settings \u2192 Tools \u2192 AI Assistant \u2192 MCP.",
                NotificationType.INFORMATION,
            )
            .notify(e.project)
    }
}

class CopyHttpConfigAction : AnAction("Copy HTTP Config", "Copy HTTP MCP configuration for AI Assistant", null) {
    override fun actionPerformed(e: AnActionEvent) {
        val config = McpSettings.getInstance().getHttpConfig()
        val clipboard = Toolkit.getDefaultToolkit().systemClipboard
        clipboard.setContents(StringSelection(config), null)

        NotificationGroupManager.getInstance()
            .getNotificationGroup("Seedance MCP")
            .createNotification(
                "HTTP config copied! Paste into Settings \u2192 Tools \u2192 AI Assistant \u2192 MCP.",
                NotificationType.INFORMATION,
            )
            .notify(e.project)
    }
}
