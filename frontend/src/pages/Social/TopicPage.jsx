import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  CircularProgress,
  Stack,
  Divider,
} from "@mui/material";
import PostBox from "../../components/forum/PostBox";
import TopicCard from "../../components/forum/TopicCard";
import api from "../../services/api";
import { useParams } from "react-router-dom";
import ReplyBox from "../../components/forum/ReplyBox";
import EditReplyDialog from "../../components/forum/EditReplyDialog";
import ConfirmDialogDelete from "../../components/forum/ConfirmDialogDelete";

export default function TopicPage() {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingReply, setDeletingReply] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleDeleteReply = (post) => {
    setDeletingReply(post);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    setDeleteLoading(true);
    try {
      await api.delete(`/api/social/replies/${deletingReply.id}`);
      setDeleteDialogOpen(false);
      setDeletingReply(null);
      reloadReplies();
    } finally {
      setDeleteLoading(false);
    }
  };
  const { topicId } = useParams();
  const [topic, setTopic] = useState(null);
  const [replies, setReplies] = useState([]);
  const [loading, setLoading] = useState(true);

  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingReply, setEditingReply] = useState(null);

  const reloadReplies = () => {
    api.get(`/api/social/topics/${topicId}/replies`).then((res) => {
      setTopic(res.data.topic);
      setReplies(res.data.replies || []);
      setLoading(false);
    });
  };

  // Modifică handlerul de edit:
  const handleEditReply = (post) => {
    setEditingReply(post);
    setEditDialogOpen(true);
  };

  const handleReportReply = async (post) => {
    const reason = prompt("Are you sure you want to report?");
    if (!reason) return;
    await api.post(`/api/social/reports`, {
      reply_id: post.id,
    });
    alert("Reply reported.");
  };

  useEffect(() => {
    reloadReplies();
  }, [topicId]);

  if (loading)
    return (
      <Box sx={{ textAlign: "center", mt: 6 }}>
        <CircularProgress />
      </Box>
    );

  return (
    <Box sx={{ p: { xs: 1, md: 3 }, bgcolor: "#181818", minHeight: "100vh" }}>
      <TopicCard
        id={topic.id}
        title={topic.title}
        imgURL={topic.imgURL}
        mediaId={topic.mediaId}
      />

      {replies.length === 0 ? (
        <Box
          sx={{
            p: 4,
            mt: 2,
            bgcolor: "#232323",
            borderRadius: 1,
            border: "1px solid #333",
            color: "#bbb",
            textAlign: "center",
            fontStyle: "italic",
          }}
        >
          No replies yet. Be the first to reply!
        </Box>
      ) : (
        replies.map((reply, idx) => (
          <PostBox
            key={reply.id}
            index={idx + 2}
            post={reply}
            onDelete={handleDeleteReply}
            onEdit={handleEditReply}
            onReport={handleReportReply}
          />
        ))
      )}

      <EditReplyDialog
        open={editDialogOpen}
        replyId={editingReply?.id}
        initialMessage={editingReply?.message}
        onClose={() => setEditDialogOpen(false)}
        onSaveSuccess={() => {
          setEditDialogOpen(false);
          setEditingReply(null);
          reloadReplies();
        }}
      />

      <ReplyBox topicId={topic.id} onReplySuccess={reloadReplies} />
      <ConfirmDialogDelete
        open={deleteDialogOpen}
        title="Delete Reply"
        content="Are you sure you want to delete?"
        onCancel={() => {
          setDeleteDialogOpen(false);
          setDeletingReply(null);
        }}
        onConfirm={confirmDelete}
        confirmText="Delete"
        cancelText="Cancel"
        loading={deleteLoading}
      />
    </Box>
  );
}
